#!/usr/bin/env python
"""Per-sample ingestion + QC: raw/ -> data/GSM9895922_processed.h5.

For this single sample
(GSM9895922, hypertensive nephropathy, LS / —, Visium spatial transcriptomics (10x Space Ranger)), parse the original author-distributed files in
``raw/`` into a standardized, QC-filtered AnnData stored under the unified name
``data/GSM9895922_processed.h5`` (h5ad-compatible HDF5), plus a matching QC report
``data/GSM9895922_processed.qc.json``.

Provenance:
  gsm        : GSM9895922
  study      : hypertensive-nephropathy (GSE339455)
  condition  : hypertensive nephropathy, LS / —
  species    : Homo sapiens
  modality   : spatial (10x Visium CytAssist)
  raw files  : GSM9895922_LS_aligned_fiducials.jpg.gz; GSM9895922_LS_aligned_tissue_image.jpg.gz; GSM9895922_LS_barcodes.tsv.gz; GSM9895922_LS_cytassist_image.tiff.gz; GSM9895922_LS_features.tsv.gz; GSM9895922_LS_matrix.mtx.gz; GSM9895922_LS_scalefactors_json.json.gz; GSM9895922_LS_tissue_hires_image.png.gz; GSM9895922_LS_tissue_lowres_image.png.gz; GSM9895922_LS_tissue_positions.csv.gz

Usage:
    process.py --raw-dir raw --data-dir data --tmp-dir tmp
"""

from __future__ import annotations

import argparse
import datetime as _dt
import gzip
import io
import json
import shutil
import sys
import tarfile
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
import scanpy as sc
import anndata as ad
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image


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
    'gsm': 'GSM9895922',
    'sample_id': 'LS (late stable)',
    'species': 'Homo sapiens',
    'gse': 'GSE339455',
    'study': 'hypertensive-nephropathy',
    'modality': 'spatial',
    'platform': '10x Visium CytAssist',
    'disease_condition': 'hypertensive nephropathy (LS)',
    'tissue_region': 'whole kidney',
    'sex': 'NA',
    'age': 'NA',
    'treatment': 'NA',
    'model_genotype': 'NA',
    'patient_individual': 'NA',
    'panel_probes': 'WTS (Visium CytAssist)',
    'prep': 'FFPE',
    'reference_genome': 'hg38',
    'condition_detail': 'hypertensive nephropathy, LS',
    'timepoint': '—',
}

# Quality control parameters (lenient thresholds for Visium / Visium HD 8µm bins)
THRESHOLDS: Dict[str, float] = {
    "min_counts_per_spot": 10,
    "min_genes_per_spot": 3,
    "min_spots_per_gene": 3,
    "keep_fraction_min": 0.30,
}


# --------------------------------------------------------------------------- #
# obs table from embedded metadata
# --------------------------------------------------------------------------- #
def build_obs(n_units: int) -> pd.DataFrame:
    """Build the standardized per-spot obs table from the embedded SAMPLE_META."""
    meta: Dict[str, Any] = dict(SAMPLE_META)
    for c in ("n_genes", "n_counts", "pct_mito", "qc_pass"):
        meta[c] = np.nan
    return pd.DataFrame([meta] * n_units)


# --------------------------------------------------------------------------- #
# File discovery + staging (extracted Visium, gzipped or plain)
# --------------------------------------------------------------------------- #
SUFFIX_MTX = {"barcodes": "barcodes.tsv.gz", "features": "features.tsv.gz", "matrix": "matrix.mtx.gz"}


def find(raw_dir: Path, gsm: str, key: str) -> Optional[Path]:
    """Locate a file for ``gsm`` by suffix keyword (barcodes/features/matrix/…)."""
    pats = {
        "barcodes": ("barcodes.tsv", "barcodes"),
        "features": ("features.tsv", "features"),
        "matrix": ("matrix.mtx", "matrix"),
        "positions": ("tissue_positions", "positions"),
        "hires": ("tissue_hires_image",),
        "lowres": ("tissue_lowres_image",),
        "scalefactors": ("scalefactors_json", "scalefactors.json"),
        "cytassist": ("cytassist_image.tiff",),
        "detected": ("detected_tissue_image",),
        "spatial_tar": ("spatial.tar",),
    }
    hits = []
    for f in sorted(raw_dir.iterdir()):
        if not f.is_file() or not f.name.startswith(f"{gsm}_"):
            continue
        for p in pats.get(key, (key,)):
            if p in f.name:
                hits.append(f)
                break
    return hits[0] if hits else None


def read_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if path.name.endswith(".gz"):
        try:
            data = gzip.decompress(data)
        except OSError:
            pass
    return data


def stage_mtx(raw_dir: Path, gsm: str, tmp_dir: Path) -> Path:
    """Copy the MTX trio to a staging dir with canonical names (gzip-normalized)."""
    stage = tmp_dir / f"{gsm}_mtx"
    stage.mkdir(parents=True, exist_ok=True)
    for key, canon in SUFFIX_MTX.items():
        src = find(raw_dir, gsm, key)
        if src is None:
            log("ERROR", f"missing {key} for {gsm} under {raw_dir}")
            sys.exit(3)
        data = src.read_bytes()
        if not src.name.endswith(".gz"):
            data = gzip.compress(data)
        (stage / canon).write_bytes(data)
    log("INFO", f"staged 10x MTX for {gsm} (3 files)")
    return stage


# --------------------------------------------------------------------------- #
# Positions / images / scalefactors
# --------------------------------------------------------------------------- #
def load_positions(path: Path) -> pd.DataFrame:
    """Read tissue positions (csv with/without header, or parquet)."""
    data = read_bytes(path)
    if path.name.endswith(".parquet") or path.name.endswith(".parquet.gz"):
        df = pd.read_parquet(io.BytesIO(data))
        return df
    try:
        first = pd.read_csv(io.BytesIO(data), nrows=1)
        if "barcode" in first.columns:
            return pd.read_csv(io.BytesIO(data))
    except Exception:
        pass
    names = ["barcode", "in_tissue", "array_row", "array_col",
             "pxl_col_in_fullres", "pxl_row_in_fullres"]
    ncols = len(pd.read_csv(io.BytesIO(data), header=None, nrows=1).columns)
    return pd.read_csv(io.BytesIO(data), header=None, names=names[:ncols])


def load_image(path: Path) -> Optional[np.ndarray]:
    """Load an image (png/tiff/jpg, possibly gzipped) into an RGB(A) array."""
    try:
        data = read_bytes(path)
        img = Image.open(io.BytesIO(data))
        return np.asarray(img.convert("RGB"))
    except Exception as e:
        log("WARN", f"could not load image {path.name}: {e}")
        return None


def load_scalefactors(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(read_bytes(path).decode())
    except Exception:
        return {}


def extract_spatial_tar(tar_path: Path, tmp_dir: Path, gsm: str) -> Path:
    """Extract positions + images + scalefactors from a per-GSM spatial.tar.gz."""
    stage = tmp_dir / f"{gsm}_spatial_tar"
    stage.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_path, "r:*") as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            if any(k in m.name for k in ("tissue_positions", "tissue_hires_image",
                                         "tissue_lowres_image", "scalefactors_json",
                                         "detected_tissue_image")):
                tf.extract(m, path=stage, filter="data")
    return stage


def read_visium_extracted(raw_dir: Path, gsm: str, tmp_dir: Path) -> ad.AnnData:
    """Assemble a Visium AnnData from extracted files; degrade gracefully."""
    stage = stage_mtx(raw_dir, gsm, tmp_dir)
    adata = sc.read_10x_mtx(str(stage), var_names="gene_symbols", make_unique=True, gex_only=True)
    library_id = gsm

    # positions / images / scalefactors
    spatial_dir: Optional[Path] = None
    st = find(raw_dir, gsm, "spatial_tar")
    if st is not None:
        spatial_dir = extract_spatial_tar(st, tmp_dir, gsm)

    pos_path = find(raw_dir, gsm, "positions")
    if pos_path is None and spatial_dir is not None:
        pos_path = next(spatial_dir.rglob("tissue_positions*.csv"), None)
    if pos_path is not None:
        try:
            pos = load_positions(pos_path)
            pos = pos.set_index("barcode").reindex(adata.obs_names)
            for c in ("in_tissue", "array_row", "array_col"):
                if c in pos.columns:
                    adata.obs[c] = pos[c].values
            if "pxl_col_in_fullres" in pos.columns and "pxl_row_in_fullres" in pos.columns:
                adata.obsm["spatial"] = pos[["pxl_col_in_fullres", "pxl_row_in_fullres"]].values.astype(float)
        except Exception as e:
            log("WARN", f"positions unreadable ({pos_path.name}): {e}")

    images: Dict[str, np.ndarray] = {}
    img_keys = ("hires", "lowres")
    for key in img_keys:
        p = find(raw_dir, gsm, key)
        if p is None and spatial_dir is not None:
            p = next(spatial_dir.rglob(f"tissue_{key}_image.png"), None)
        if p is not None:
            img = load_image(p)
            if img is not None:
                images[key] = img
    if not images:
        p = find(raw_dir, gsm, "cytassist") or find(raw_dir, gsm, "detected")
        if p is not None:
            img = load_image(p)
            if img is not None:
                images["hires"] = img

    scalefactors: Dict[str, Any] = {}
    sf = find(raw_dir, gsm, "scalefactors")
    if sf is None and spatial_dir is not None:
        sf = next(spatial_dir.rglob("scalefactors_json.json"), None)
    if sf is not None:
        scalefactors = load_scalefactors(sf)

    if images or "spatial" in adata.obsm:
        adata.uns["spatial"] = {library_id: {"images": images, "scalefactors": scalefactors}}

    adata.var["feature_type"] = "Gene Expression"
    adata.var["genome"] = "hg38" if SAMPLE_META.get("species") == "Homo sapiens" else "mm10"
    return adata


# --------------------------------------------------------------------------- #
# QC
# --------------------------------------------------------------------------- #
MITO_PATTERNS = {"Homo sapiens": r"^MT-", "Mus musculus": r"^mt-"}


def compute_spot_qc(adata: ad.AnnData, mito_pat: str) -> ad.AnnData:
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
    compute_spot_qc(adata, MITO_PATTERNS.get(species, r"^MT-"))
    mask = pd.Series(True, index=adata.obs_names)
    if "min_genes_per_spot" in thr:
        mask &= adata.obs["n_genes"] >= thr["min_genes_per_spot"]
    if "min_counts_per_spot" in thr:
        mask &= adata.obs["n_counts"] >= thr["min_counts_per_spot"]
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
        "gsm": None, "assay": "Visium", "species": species,
        "pre_cells": pre_cells, "pre_genes": pre_genes,
        "post_cells": post_cells, "post_genes": post_genes,
        "keep_fraction": round(keep_frac, 4),
        "median_genes_per_unit": float(np.median(clean.obs["n_genes"])) if post_cells else np.nan,
        "median_counts_per_unit": float(np.median(clean.obs["n_counts"])) if post_cells else np.nan,
        "median_pct_mito": float(np.median(clean.obs["pct_mito"])) if post_cells else np.nan,
        "qc_pass": not warn,
        "qc_note": (f"pre {pre_cells} units / {pre_genes} genes -> post {post_cells} units / "
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
        f"  units             : {metrics['pre_cells']}",
        f"  genes             : {metrics['pre_genes']}",
        "", "  --- Post-QC (filtered) ---",
        f"  units             : {metrics['post_cells']}   (kept {metrics['keep_fraction']:.1%})",
        f"  genes             : {metrics['post_genes']}",
        f"  median genes/unit : {fmt(metrics['median_genes_per_unit'])}",
        f"  median counts/unit: {fmt(metrics['median_counts_per_unit'])}",
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
    """UMI-counts figure: overlay on tissue image when possible, else scatter/hist."""
    has_spatial = "spatial" in adata.obsm
    images = {}
    if "spatial" in adata.uns:
        images = next(iter(adata.uns["spatial"].values())).get("images", {})
    if has_spatial and images:
        img = images.get("hires")
        if img is None:
            img = images.get("lowres")
        scalef = next(iter(adata.uns["spatial"].values())).get("scalefactors", {})
        if img is not None:
            fig, ax = plt.subplots(1, 1, figsize=(9, 9))
            spot = float(scalef.get("spot_diameter_fullres", 1.0) * scalef.get("tissue_hires_scalef", 1.0)) or 1.0
            sc.pl.spatial(adata, color="n_counts", img_key="hires" if "hires" in images else "lowres",
                          spot_size=spot, title=f"{gsm} — UMI counts", ax=ax, show=False, color_map="magma")
            fig.savefig(str(out_png), dpi=200, bbox_inches="tight")
            plt.close(fig)
            log("INFO", f"wrote {out_png} (image overlay)")
            return
    if has_spatial:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        sc_ = ax.scatter(adata.obsm["spatial"][:, 0], adata.obsm["spatial"][:, 1],
                         c=np.log1p(adata.obs["n_counts"]), cmap="magma", s=2, alpha=0.8)
        plt.colorbar(sc_, ax=ax, label="log1p(UMI counts)")
        ax.set_title(f"{gsm} — UMI counts (no tissue image)")
        ax.set_aspect("equal"); ax.axis("off")
        fig.savefig(str(out_png), dpi=200, bbox_inches="tight")
        plt.close(fig)
        log("INFO", f"wrote {out_png} (scatter, no image)")
        return
    # no spatial coordinates -> counts summary histogram
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    ax.hist(np.log1p(adata.obs["n_counts"]), bins=50, color="slategray")
    ax.set_xlabel("log1p(UMI counts)"); ax.set_ylabel("units")
    ax.set_title(f"{gsm} — UMI counts distribution (no spatial positions)")
    fig.tight_layout(); fig.savefig(str(out_png), dpi=200, bbox_inches="tight"); plt.close(fig)
    log("INFO", f"wrote {out_png} (counts histogram, no positions)")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--gsm", default=SAMPLE_META["gsm"], help="GEO sample accession")
    p.add_argument("--raw-dir", default="raw", help="read-only original files (extracted Visium)")
    p.add_argument("--raw-out", default="raw", help="output directory for pre-QC counts file")
    p.add_argument("--data-dir", default="data", help="output dir for processed.h5 / qc.* / umi figure")
    p.add_argument("--tmp-dir", default="tmp", help="temporary working directory")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    gsm = SAMPLE_META["gsm"]
    log("INFO", f"process start for {gsm} (Visium-extracted)")

    raw_dir = Path(args.raw_dir)
    raw_out = Path(args.raw_out)
    data_dir = Path(args.data_dir)
    tmp_dir = Path(args.tmp_dir)
    raw_out.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    raw_files = [p.name for p in raw_dir.iterdir()
                 if p.is_file() and not p.name.endswith("_raw_counts.h5")]
    adata = read_visium_extracted(raw_dir, gsm, tmp_dir)

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
        "script": "process.py (visium_extracted variant)",
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
