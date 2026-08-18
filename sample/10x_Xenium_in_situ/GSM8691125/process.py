#!/usr/bin/env python
"""Per-sample ingestion + QC: raw/ -> data/GSM8691125_processed.h5.

For this single sample
(GSM8691125, allogeneic, C57BL/6→BALB/c / —, Xenium in situ spatial transcriptomics), parse the original author-distributed files in
``raw/`` into a standardized, QC-filtered AnnData stored under the unified name
``data/GSM8691125_processed.h5`` (h5ad-compatible HDF5), plus a matching QC report
``data/GSM8691125_processed.qc.json``.

Provenance:
  gsm        : GSM8691125
  study      : kidney-transplant-rejection (GSE284742)
  condition  : allogeneic, C57BL/6→BALB/c / —
  species    : Mus musculus
  modality   : spatial (10x Xenium in situ)
  raw files  : GSM8691125_bl6.bc.3.morphology.ome.tif.gz; GSM8691125_bl6.bc.3.transcripts.zarr.zip

Usage:
    process.py --raw-dir raw --data-dir data --tmp-dir tmp
"""

from __future__ import annotations

import argparse
import datetime as _dt
import gzip
import json
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
import scipy.sparse as sp
import scanpy as sc
import anndata as ad
import zarr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
def log(level: str, msg: str) -> None:
    ts = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)


# --------------------------------------------------------------------------- #
# Sample metadata & QC parameters
# --------------------------------------------------------------------------- #
# Sample metadata
SAMPLE_META: Dict[str, str] = {
    'gsm': 'GSM8691125',
    'sample_id': 'B6→BALB/c allo 3 (Xenium)',
    'species': 'Mus musculus',
    'gse': 'GSE284742',
    'study': 'kidney-transplant-rejection',
    'modality': 'spatial',
    'platform': '10x Xenium in situ',
    'disease_condition': 'transplant (syn/allo, mouse)',
    'tissue_region': 'whole kidney (transplant)',
    'sex': 'NA',
    'age': 'NA',
    'treatment': 'NA',
    'model_genotype': 'C57BL/6 / BALB/c donor→recipient',
    'patient_individual': 'NA',
    'panel_probes': 'Xenium (panel ?)',
    'prep': 'FFPE',
    'reference_genome': 'mm10',
    'condition_detail': 'allogeneic, C57BL/6→BALB/c',
    'timepoint': '—',
}

# Quality control parameters
THRESHOLDS: Dict[str, float] = {
    "min_counts_per_spot": 5,
    "min_genes_per_spot": 2,
    "min_spots_per_gene": 3,
    "keep_fraction_min": 0.30,
}
BIN_SIZE_UM: float = 25.0


# --------------------------------------------------------------------------- #
# obs table from embedded metadata
# --------------------------------------------------------------------------- #
def build_obs(n_units: int) -> pd.DataFrame:
    meta: Dict[str, Any] = dict(SAMPLE_META)
    for c in ("n_genes", "n_counts", "pct_mito", "qc_pass"):
        meta[c] = np.nan
    return pd.DataFrame([meta] * n_units)


# --------------------------------------------------------------------------- #
# Transcript binning
# --------------------------------------------------------------------------- #
def unzip_zarr(raw_dir: Path, gsm: str, tmp_dir: Path) -> Path:
    zip_path = next(raw_dir.glob(f"{gsm}*transcripts.zarr.zip"), None)
    if zip_path is None:
        log("ERROR", f"no transcripts.zarr.zip for {gsm} under {raw_dir}")
        sys.exit(3)
    zdir = tmp_dir / f"{gsm}_zarr"
    if not zdir.exists():
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(zdir)
        log("INFO", f"unzipped {zip_path.name} -> {zdir}")
    return zdir


def iter_tiles(store: zarr.Group):
    for fov in sorted(store["grids"].keys(), key=int):
        for tile in sorted(store["grids"][fov].keys()):
            grp = store["grids"][fov][tile]
            yield fov, tile, grp


def read_valid(grp):
    """Return (x, y, gene_idx) for valid transcripts in one tile."""
    loc = np.asarray(grp["location"][:])            # (N,3) µm
    gene = np.asarray(grp["gene_identity"][:]).ravel()
    valid = np.asarray(grp["valid"][:]).ravel()
    m = valid == 1
    return loc[m, 0].astype(np.float64), loc[m, 1].astype(np.float64), gene[m].astype(np.int64)


def bin_transcripts(zdir: Path, bin_size: float, n_genes: int) -> Tuple[sp.csr_matrix, np.ndarray, np.ndarray]:
    """Bin valid transcripts into a µm grid -> (counts csr, bin_x, bin_y)."""
    store = zarr.open(str(zdir), mode="r")
    # pass 1: bounds of valid transcripts
    xmin = ymin = np.inf
    xmax = ymax = -np.inf
    for fov, tile, grp in iter_tiles(store):
        x, y, _ = read_valid(grp)
        if x.size == 0:
            continue
        xmin, xmax = min(xmin, x.min()), max(xmax, x.max())
        ymin, ymax = min(ymin, y.min()), max(ymax, y.max())
    if not np.isfinite(xmin):
        log("ERROR", "no valid transcripts found"); sys.exit(3)
    nx = int(np.floor((xmax - xmin) / bin_size)) + 1
    ny = int(np.floor((ymax - ymin) / bin_size)) + 1
    log("INFO", f"bounds x[{xmin:.0f},{xmax:.0f}] y[{ymin:.0f},{ymax:.0f}] -> bins {nx}x{ny}")

    # pass 2: accumulate counts (flattened bin-gene index)
    counts = np.zeros(nx * ny * n_genes, dtype=np.float64)
    for fov, tile, grp in iter_tiles(store):
        x, y, g = read_valid(grp)
        if x.size == 0:
            continue
        bx = np.floor((x - xmin) / bin_size).astype(np.int64)
        by = np.floor((y - ymin) / bin_size).astype(np.int64)
        flat = (by * nx + bx) * n_genes + g
        np.add.at(counts, flat, 1.0)
    counts = counts.reshape(nx * ny, n_genes)
    # keep only non-empty bins
    nz = np.asarray(counts.sum(axis=1) > 0)
    bin_idx = np.flatnonzero(nz)
    mat = sp.csr_matrix(counts[nz])
    bx = (bin_idx % nx).astype(float) * bin_size + xmin + bin_size / 2
    by = (bin_idx // nx).astype(float) * bin_size + ymin + bin_size / 2
    log("INFO", f"built {mat.shape[0]} non-empty bins x {n_genes} genes")
    return mat, bx, by


def read_xenium_zarr(raw_dir: Path, gsm: str, tmp_dir: Path, bin_size: float) -> ad.AnnData:
    zdir = unzip_zarr(raw_dir, gsm, tmp_dir)
    store = zarr.open(str(zdir), mode="r")
    attrs = dict(store.attrs)
    gene_names = np.asarray(attrs.get("gene_names", []))
    if gene_names.size == 0:
        log("ERROR", "no gene_names in zarr attrs"); sys.exit(3)
    counts, bx, by = bin_transcripts(zdir, bin_size, len(gene_names))
    adata = ad.AnnData(X=counts, var=pd.DataFrame(index=gene_names))
    adata.obsm["spatial"] = np.column_stack([bx, by])
    adata.var["feature_type"] = "Gene Expression"
    adata.var["genome"] = "hg38" if SAMPLE_META.get("species") == "Homo sapiens" else "mm10"
    return adata


# --------------------------------------------------------------------------- #
# QC
# --------------------------------------------------------------------------- #
def compute_spot_qc(adata: ad.AnnData) -> ad.AnnData:
    adata.obs["n_genes"] = np.asarray((adata.X > 0).sum(axis=1)).ravel()
    adata.obs["n_counts"] = np.asarray(adata.X.sum(axis=1)).ravel()
    adata.obs["pct_mito"] = 0.0
    return adata


def run_qc(adata: ad.AnnData, thr: Dict[str, Any]) -> Tuple[Dict[str, Any], ad.AnnData]:
    pre_cells, pre_genes = adata.n_obs, adata.n_vars
    compute_spot_qc(adata)
    mask = pd.Series(True, index=adata.obs_names)
    if "min_genes_per_spot" in thr:
        mask &= adata.obs["n_genes"] >= thr["min_genes_per_spot"]
    if "min_counts_per_spot" in thr:
        mask &= adata.obs["n_counts"] >= thr["min_counts_per_spot"]
    adata.obs["qc_pass"] = mask.values
    n_pass = int(mask.sum())
    keep_frac = n_pass / max(pre_cells, 1)
    clean = adata[mask].copy()
    min_cells = thr.get("min_cells_per_gene", thr.get("min_spots_per_gene", 0))
    if min_cells:
        clean.var["n_cells"] = np.asarray((clean.X > 0).sum(axis=0)).ravel()
        clean = clean[:, clean.var["n_cells"] >= min_cells].copy()
    post_cells, post_genes = clean.n_obs, clean.n_vars
    warn = keep_frac < thr.get("keep_fraction_min", 0.0)
    metrics = {
        "gsm": None, "assay": "Xenium (binned)", "species": SAMPLE_META.get("species", "NA"),
        "pre_cells": pre_cells, "pre_genes": pre_genes,
        "post_cells": post_cells, "post_genes": post_genes,
        "keep_fraction": round(keep_frac, 4),
        "median_genes_per_unit": float(np.median(clean.obs["n_genes"])) if post_cells else np.nan,
        "median_counts_per_unit": float(np.median(clean.obs["n_counts"])) if post_cells else np.nan,
        "median_pct_mito": 0.0,
        "qc_pass": not warn,
        "qc_note": (f"pre {pre_cells} bins / {pre_genes} genes -> post {post_cells} bins / "
                    f"{post_genes} genes (kept {keep_frac:.1%})"
                    + ("; WARN low retained fraction" if warn else "")),
    }
    return metrics, clean


# --------------------------------------------------------------------------- #
# Outputs
# --------------------------------------------------------------------------- #
def fmt(x: Any) -> str:
    try:
        return f"{float(x):.2f}" if np.isfinite(float(x)) else "n/a"
    except (TypeError, ValueError):
        return str(x)


def write_qc_report(gsm: str, metrics: Dict[str, Any], thr: Dict[str, Any],
                    raw_files: "list[str]", out_txt: Path) -> None:
    meta = SAMPLE_META
    bar = "=" * 78
    lines = [
        bar, f"  QC REPORT — {gsm}  (Xenium transcripts.zarr, {BIN_SIZE_UM:.0f} µm bins)", bar,
        f"  Study             : {meta.get('study', 'NA')} ({meta.get('gse', 'NA')})",
        f"  Condition         : {meta.get('condition_detail', 'NA')} / {meta.get('timepoint', 'NA')}",
        f"  Species           : {meta.get('species', 'NA')}",
        f"  Assay / Platform  : {metrics['assay']} / {meta.get('platform', 'NA')}",
        f"  Source (raw/)     : {', '.join(raw_files) or 'NA'}",
        "", "  --- Pre-QC (binned) ---",
        f"  bins              : {metrics['pre_cells']}",
        f"  genes             : {metrics['pre_genes']}",
        "", "  --- Post-QC (filtered) ---",
        f"  bins              : {metrics['post_cells']}   (kept {metrics['keep_fraction']:.1%})",
        f"  genes             : {metrics['post_genes']}",
        f"  median genes/bin  : {fmt(metrics['median_genes_per_unit'])}",
        f"  median counts/bin : {fmt(metrics['median_counts_per_unit'])}",
        "", "  --- Thresholds applied ---",
    ]
    lines += [f"  {k:<24}: {v}" for k, v in thr.items()]
    lines += [
        "", f"  QC result         : {'PASS' if metrics['qc_pass'] else 'WARN'}",
        f"  Note              : {metrics['qc_note']}",
        "",
        f"  Outputs : data/{gsm}_processed.h5 · data/{gsm}_processed.qc.json · data/{gsm}_umi_counts.png",
        f"  Raw counts (pre-QC) : raw/{gsm}_raw_counts.h5",
        f"  Generated : {_dt.datetime.now().isoformat()}  (process.py)",
        bar,
    ]
    out_txt.write_text("\n".join(lines) + "\n")
    log("INFO", f"wrote {out_txt}")


def plot_umi_overlay(adata: ad.AnnData, gsm: str, out_png: Path) -> None:
    fig, ax = plt.subplots(1, 1, figsize=(9, 9))
    sc_ = ax.scatter(adata.obsm["spatial"][:, 0], adata.obsm["spatial"][:, 1],
                     c=np.log1p(adata.obs["n_counts"]), cmap="magma", s=1.0, alpha=0.8, rasterized=True)
    plt.colorbar(sc_, ax=ax, label="log1p(transcripts/bin)")
    ax.set_title(f"{gsm} — transcript counts per {BIN_SIZE_UM:.0f}µm bin")
    ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout(); fig.savefig(str(out_png), dpi=200, bbox_inches="tight"); plt.close(fig)
    log("INFO", f"wrote {out_png}")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--gsm", default=SAMPLE_META["gsm"], help="GEO sample accession")
    p.add_argument("--raw-dir", default="raw", help="read-only original files (transcripts.zarr.zip)")
    p.add_argument("--raw-out", default="raw", help="output directory for pre-QC counts file")
    p.add_argument("--data-dir", default="data", help="output dir for processed.h5 / qc.* / umi figure")
    p.add_argument("--tmp-dir", default="tmp", help="temporary working directory")
    p.add_argument("--bin-size", type=float, default=BIN_SIZE_UM, help="bin size in µm")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    gsm = SAMPLE_META["gsm"]
    log("INFO", f"process start for {gsm} (Xenium zarr, bin={args.bin_size}µm)")

    raw_dir = Path(args.raw_dir)
    raw_out = Path(args.raw_out)
    data_dir = Path(args.data_dir)
    tmp_dir = Path(args.tmp_dir)
    raw_out.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    raw_files = [p.name for p in raw_dir.iterdir()
                 if p.is_file() and not p.name.endswith("_raw_counts.h5")]
    adata = read_xenium_zarr(raw_dir, gsm, tmp_dir, args.bin_size)

    raw_counts_adata = adata.copy()
    raw_counts_adata.write_h5ad(str(raw_out / f"{gsm}_raw_counts.h5"))
    log("INFO", f"wrote raw counts (pre-QC) {raw_out / f'{gsm}_raw_counts.h5'} ({raw_counts_adata.n_obs} x {raw_counts_adata.n_vars})")

    metrics, clean = run_qc(adata, THRESHOLDS)

    meta_obs = build_obs(clean.n_obs)
    for c in ("n_genes", "n_counts", "pct_mito"):
        meta_obs[c] = clean.obs[c].values if c in clean.obs else np.nan
    meta_obs["qc_pass"] = clean.obs["qc_pass"].values
    for c in clean.obs.columns:
        if c not in meta_obs.columns:
            meta_obs[c] = clean.obs[c].values
    clean.obs = meta_obs
    clean.obs_names_make_unique()
    clean.uns["gsm"] = gsm
    clean.uns["qc"] = metrics
    clean.uns["processing"] = {
        "script": "process.py (xenium_zarr variant)",
        "thresholds": THRESHOLDS,
        "bin_size_um": args.bin_size,
        "metadata_source": "SAMPLE_META",
        "timestamp": _dt.datetime.now().isoformat(),
    }

    out_h5 = data_dir / f"{gsm}_processed.h5"
    clean.write_h5ad(str(out_h5))
    log("INFO", f"wrote {out_h5} ({clean.n_obs} x {clean.n_vars})")

    metrics["gsm"] = gsm
    out_qc = data_dir / f"{gsm}_processed.qc.json"
    with open(out_qc, "w") as f:
        json.dump(metrics, f, indent=2)
    log("INFO", f"wrote {out_qc}")

    write_qc_report(gsm, metrics, THRESHOLDS, raw_files, data_dir / f"{gsm}_qc_report.txt")
    plot_umi_overlay(clean, gsm, data_dir / f"{gsm}_umi_counts.png")

    log("INFO", f"process done for {gsm}: {metrics['qc_note']}")


if __name__ == "__main__":
    main()
