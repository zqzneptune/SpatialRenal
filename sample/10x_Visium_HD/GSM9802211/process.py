#!/usr/bin/env python
"""Per-sample ingestion + QC: raw/ -> data/GSM9802211_processed.h5.

For this single sample
(GSM9802211, chronic AMR graft biopsy / —, Visium spatial transcriptomics (10x Space Ranger)), parse the original author-distributed files in
``raw/`` into a standardized, QC-filtered AnnData stored under the unified name
``data/GSM9802211_processed.h5`` (h5ad-compatible HDF5), plus a matching QC report
``data/GSM9802211_processed.qc.json``.

Provenance:
  gsm        : GSM9802211
  study      : CAMR-scRNA-VisiumHD (GSE334924)
  condition  : chronic AMR graft biopsy / —
  species    : Homo sapiens
  modality   : spatial (10x Visium HD)
  raw files  : GSM9802211_CAMR-ZLD_Spatial.tar.gz

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
import tarfile
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
import scanpy as sc
import anndata as ad
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.image import imread


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
    'gsm': 'GSM9802211',
    'sample_id': 'CAMR-ZLD_Spatial',
    'species': 'Homo sapiens',
    'gse': 'GSE334924',
    'study': 'CAMR-scRNA-VisiumHD',
    'modality': 'spatial',
    'platform': '10x Visium HD',
    'disease_condition': 'transplant-CAMR',
    'tissue_region': 'whole kidney',
    'sex': 'M',
    'age': '40 years',
    'treatment': 'Tacrolimus + MMF + corticosteroids',
    'model_genotype': 'NA',
    'patient_individual': 'CAMR-ZLD',
    'panel_probes': 'WTS (Visium HD)',
    'prep': 'NA',
    'reference_genome': 'hg38',
    'condition_detail': 'chronic AMR graft biopsy',
    'timepoint': '—',
}

# Quality control parameters
THRESHOLDS: Dict[str, float] = {
    "min_counts_per_cell": 10,
    "min_genes_per_cell": 3,
    "min_cells_per_gene": 10,
    "keep_fraction_min": 0.50,
}


# --------------------------------------------------------------------------- #
# obs table from embedded metadata
# --------------------------------------------------------------------------- #
def build_obs(n_units: int) -> pd.DataFrame:
    meta: Dict[str, Any] = dict(SAMPLE_META)
    for c in ("n_genes", "n_counts", "pct_mito", "qc_pass"):
        meta[c] = np.nan
    return pd.DataFrame([meta] * n_units)


# --------------------------------------------------------------------------- #
# Stage + read Visium HD (cell segmentation)
# --------------------------------------------------------------------------- #
def stage_tar(raw_dir: Path, gsm: str, tmp_dir: Path) -> Path:
    tars = [p for p in sorted(raw_dir.glob(f"{gsm}*")) if p.suffix == ".gz"]
    if not tars:
        log("ERROR", f"no Spatial tar for {gsm} under {raw_dir}")
        sys.exit(3)
    stage = tmp_dir / f"{gsm}_vhd"
    if not (stage / "CAMR-ZLD_Spatial").exists():
        with tarfile.open(tars[0], "r:*") as tf:
            names = [m.name for m in tf.getmembers()
                     if m.isfile() and (
                         "filtered_feature_cell_matrix/" in m.name
                         or m.name.endswith(("cell_segmentations.geojson", "tissue_hires_image.png",
                                             "tissue_lowres_image.png", "scalefactors_json.json")))]
            for m in names:
                tf.extract(m, path=stage, filter="data")
        log("INFO", f"extracted Visium HD essentials from {tars[0].name} ({len(names)} files)")
    return stage


def read_visiumhd(raw_dir: Path, gsm: str, tmp_dir: Path) -> ad.AnnData:
    stage = stage_tar(raw_dir, gsm, tmp_dir)
    root = stage / "CAMR-ZLD_Spatial"

    mtx_dir = root / "segmented_outputs" / "filtered_feature_cell_matrix"
    adata = sc.read_10x_mtx(str(mtx_dir), var_names="gene_symbols", make_unique=True, gex_only=True)
    log("INFO", f"read cell matrix {adata.n_obs} x {adata.n_vars}")

    # cell_id -> centroid from the geojson polygons
    geojson = root / "segmented_outputs" / "cell_segmentations.geojson"
    if geojson.exists():
        feats = json.load(open(geojson))["features"]
        cell2xy = {}
        for f in feats:
            cid = f["properties"].get("cell_id")
            coords = f["geometry"]["coordinates"][0]
            arr = np.asarray(coords, dtype=float)
            cell2xy[cid] = (arr[:, 0].mean(), arr[:, 1].mean())
        # barcodes are "cellid_%09d-1"
        ids = adata.obs_names.str.extract(r"cellid_(\d+)-\d+").astype(float).iloc[:, 0].values
        xy = np.array([cell2xy.get(int(i), [np.nan, np.nan]) for i in ids], dtype=float)
        valid = ~np.isnan(xy[:, 0])
        log("INFO", f"matched {int(valid.sum())}/{adata.n_obs} cells to segmentations")
        if valid.any():
            adata.obsm["spatial"] = xy
            adata.obs["has_segmentation"] = valid.astype(int)
    else:
        log("WARN", "cell_segmentations.geojson not found; no spatial coordinates")

    images: Dict[str, np.ndarray] = {}
    for key, fname in (("hires", "tissue_hires_image.png"), ("lowres", "tissue_lowres_image.png")):
        f = root / "spatial" / fname
        if f.exists():
            images[key] = imread(f)
    scalefactors: Dict[str, Any] = {}
    sf = root / "spatial" / "scalefactors_json.json"
    if sf.exists():
        scalefactors = json.load(open(sf))
    if images or "spatial" in adata.obsm:
        adata.uns["spatial"] = {gsm: {"images": images, "scalefactors": scalefactors}}

    adata.var["feature_type"] = "Gene Expression"
    adata.var["genome"] = "hg38" if SAMPLE_META.get("species") == "Homo sapiens" else "mm10"
    return adata


# --------------------------------------------------------------------------- #
# QC
# --------------------------------------------------------------------------- #
MITO_PATTERNS = {"Homo sapiens": r"^MT-", "Mus musculus": r"^mt-"}


def compute_cell_qc(adata: ad.AnnData, mito_pat: str) -> ad.AnnData:
    mito = adata.var_names.str.contains(mito_pat, regex=True, na=False)
    adata.obs["n_genes"] = np.asarray((adata.X > 0).sum(axis=1)).ravel()
    adata.obs["n_counts"] = np.asarray(adata.X.sum(axis=1)).ravel()
    if mito.any():
        mito_counts = np.asarray(adata[:, mito].X.sum(axis=1)).ravel()
        adata.obs["pct_mito"] = 100.0 * mito_counts / np.maximum(adata.obs["n_counts"].values, 1)
    else:
        adata.obs["pct_mito"] = 0.0
    return adata


def run_qc(adata: ad.AnnData, species: str, thr: Dict[str, Any]) -> Tuple[Dict[str, Any], ad.AnnData]:
    pre_cells, pre_genes = adata.n_obs, adata.n_vars
    compute_cell_qc(adata, MITO_PATTERNS.get(species, r"^MT-"))
    mask = pd.Series(True, index=adata.obs_names)
    if "min_genes_per_cell" in thr:
        mask &= adata.obs["n_genes"] >= thr["min_genes_per_cell"]
    if "min_counts_per_cell" in thr:
        mask &= adata.obs["n_counts"] >= thr["min_counts_per_cell"]
    if "max_pct_mito" in thr:
        mask &= adata.obs["pct_mito"] <= thr["max_pct_mito"]
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
        "gsm": None, "assay": "Visium HD", "species": species,
        "pre_cells": pre_cells, "pre_genes": pre_genes,
        "post_cells": post_cells, "post_genes": post_genes,
        "keep_fraction": round(keep_frac, 4),
        "median_genes_per_unit": float(np.median(clean.obs["n_genes"])) if post_cells else np.nan,
        "median_counts_per_unit": float(np.median(clean.obs["n_counts"])) if post_cells else np.nan,
        "median_pct_mito": float(np.median(clean.obs["pct_mito"])) if post_cells else np.nan,
        "qc_pass": not warn,
        "qc_note": (f"pre {pre_cells} cells / {pre_genes} genes -> post {post_cells} cells / "
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
        bar, f"  QC REPORT — {gsm}", bar,
        f"  Study             : {meta.get('study', 'NA')} ({meta.get('gse', 'NA')})",
        f"  Condition         : {meta.get('condition_detail', 'NA')} / {meta.get('timepoint', 'NA')}",
        f"  Species           : {meta.get('species', 'NA')}",
        f"  Assay / Platform  : {metrics['assay']} / {meta.get('platform', 'NA')}",
        f"  Source (raw/)     : {', '.join(raw_files) or 'NA'}",
        "", "  --- Pre-QC ---",
        f"  cells             : {metrics['pre_cells']}",
        f"  genes             : {metrics['pre_genes']}",
        "", "  --- Post-QC (filtered) ---",
        f"  cells             : {metrics['post_cells']}   (kept {metrics['keep_fraction']:.1%})",
        f"  genes             : {metrics['post_genes']}",
        f"  median genes/cell : {fmt(metrics['median_genes_per_unit'])}",
        f"  median counts/cell: {fmt(metrics['median_counts_per_unit'])}",
        f"  median % mito     : {fmt(metrics['median_pct_mito'])}",
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
    images = {}
    if "spatial" in adata.uns:
        images = next(iter(adata.uns["spatial"].values())).get("images", {})
    if "spatial" in adata.obsm and images:
        scalef = next(iter(adata.uns["spatial"].values())).get("scalefactors", {})
        img = images.get("hires")
        if img is None:
            img = images.get("lowres")
        spot = float(scalef.get("spot_diameter_fullres", 1.0) * scalef.get("tissue_hires_scalef", 1.0)) or 1.0
        fig, ax = plt.subplots(1, 1, figsize=(9, 9))
        sc.pl.spatial(adata, color="n_counts", img_key="hires" if "hires" in images else "lowres",
                      spot_size=spot, title=f"{gsm} — UMI counts per cell", ax=ax, show=False, color_map="magma")
        fig.savefig(str(out_png), dpi=200, bbox_inches="tight"); plt.close(fig)
        log("INFO", f"wrote {out_png} (image overlay)")
        return
    if "spatial" in adata.obsm:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        sc_ = ax.scatter(adata.obsm["spatial"][:, 0], adata.obsm["spatial"][:, 1],
                         c=np.log1p(adata.obs["n_counts"]), cmap="magma", s=0.6, alpha=0.7, rasterized=True)
        plt.colorbar(sc_, ax=ax, label="log1p(UMI counts)")
        ax.set_title(f"{gsm} — UMI counts per cell (no image)")
        ax.set_aspect("equal"); ax.axis("off")
        fig.savefig(str(out_png), dpi=200, bbox_inches="tight"); plt.close(fig)
        log("INFO", f"wrote {out_png} (scatter, no image)")
        return
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    ax.hist(np.log1p(adata.obs["n_counts"]), bins=50, color="slategray")
    ax.set_xlabel("log1p(UMI counts)"); ax.set_ylabel("cells")
    ax.set_title(f"{gsm} — UMI counts distribution")
    fig.tight_layout(); fig.savefig(str(out_png), dpi=200, bbox_inches="tight"); plt.close(fig)
    log("INFO", f"wrote {out_png} (counts histogram)")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--gsm", default=SAMPLE_META["gsm"], help="GEO sample accession")
    p.add_argument("--raw-dir", default="raw", help="read-only original files (Spatial tar)")
    p.add_argument("--raw-out", default="raw", help="output directory for pre-QC counts file")
    p.add_argument("--data-dir", default="data", help="output dir for processed.h5 / qc.* / umi figure")
    p.add_argument("--tmp-dir", default="tmp", help="temporary working directory")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    gsm = SAMPLE_META["gsm"]
    log("INFO", f"process start for {gsm} (Visium HD)")

    raw_dir = Path(args.raw_dir)
    raw_out = Path(args.raw_out)
    data_dir = Path(args.data_dir)
    tmp_dir = Path(args.tmp_dir)
    raw_out.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    raw_files = [p.name for p in raw_dir.iterdir()
                 if p.is_file() and not p.name.endswith("_raw_counts.h5")]
    adata = read_visiumhd(raw_dir, gsm, tmp_dir)

    raw_counts_adata = adata.copy()
    raw_counts_adata.uns.pop("spatial", None)
    raw_counts_adata.write_h5ad(str(raw_out / f"{gsm}_raw_counts.h5"))
    log("INFO", f"wrote raw counts (pre-QC) {raw_out / f'{gsm}_raw_counts.h5'} ({raw_counts_adata.n_obs} x {raw_counts_adata.n_vars})")

    species = SAMPLE_META.get("species", "NA")
    metrics, clean = run_qc(adata, species, THRESHOLDS)

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
        "script": "process.py (visiumhd_feature_slice variant)",
        "thresholds": THRESHOLDS,
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
