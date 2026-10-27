#!/usr/bin/env python
from __future__ import annotations

import argparse
import datetime as _dt
import gzip
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
import scanpy as sc
import anndata as ad
from matplotlib.image import imread
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def log(level: str, msg: str) -> None:
    ts = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)

SAMPLE_META: Dict[str, str] = {
    "gsm": "GSM10122934",
    "sample_id": "mouse_47822-7_ctrl",
    "species": "Mus musculus",
    "study": "mouse-lithium-polyuria",
    "modality": "spatial",
    "platform": "10x Visium HD",
    "gse": "GSE350835",
    "disease_condition": "reference/normal",
    "tissue_region": "whole kidney",
    "sex": "NA",
    "age": "NA",
    "treatment": "control",
    "model_genotype": "wild type",
    "patient_individual": "mouse_47822-7",
    "panel_probes": "WTS (Visium HD)",
    "prep": "FFPE",
    "reference_genome": "mm10",
    "condition_detail": "wild type mouse kidney control",
    "timepoint": "\u2014",
    "data_status": "staged"
}

THRESHOLDS: Dict[str, float] = {
    "min_counts_per_cell": 10,
    "min_genes_per_cell": 3,
    "min_cells_per_gene": 10,
    "max_pct_mito": 30.0,
    "keep_fraction_min": 0.50,
}

def build_obs(n_units: int) -> pd.DataFrame:
    meta: Dict[str, Any] = dict(SAMPLE_META)
    for c in ("n_genes", "n_counts", "pct_mito", "qc_pass"):
        meta[c] = np.nan
    return pd.DataFrame([meta] * n_units)

def read_visiumhd(raw_dir: Path, gsm: str) -> ad.AnnData:
    h5s = sorted(raw_dir.glob(f"{gsm}_*cell_filtered_feature_cell_matrix.h5"))
    if not h5s:
        log("ERROR", f"no cell_filtered_feature_cell_matrix.h5 for {gsm} under {raw_dir}")
        sys.exit(3)
    adata = sc.read_10x_h5(str(h5s[0]))
    adata.var_names_make_unique()
    log("INFO", f"read cell matrix {adata.n_obs} x {adata.n_vars}")

    geojsons = sorted(raw_dir.glob(f"{gsm}_*cell_segmentations.geojson*"))
    if geojsons:
        gj = geojsons[0]
        if gj.name.endswith(".gz"):
            with gzip.open(gj, "rt") as f:
                feats = json.load(f)["features"]
        else:
            with open(gj) as f:
                feats = json.load(f)["features"]
        cell2xy = {}
        for f in feats:
            cid = f["properties"].get("cell_id")
            coords = f["geometry"]["coordinates"][0]
            arr = np.asarray(coords, dtype=float)
            cell2xy[cid] = (arr[:, 0].mean(), arr[:, 1].mean())
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
    for key, pat in (("hires", "*tissue_hires_image.png*"), ("lowres", "*tissue_lowres_image.png*")):
        hits = sorted(raw_dir.glob(f"{gsm}_{pat}"))
        if hits:
            try:
                images[key] = imread(hits[0])
            except Exception:
                pass
    scalefactors: Dict[str, Any] = {}
    sf_hits = sorted(raw_dir.glob(f"{gsm}_*scalefactors_json.json*"))
    if sf_hits:
        try:
            if sf_hits[0].name.endswith(".gz"):
                scalefactors = json.load(gzip.open(sf_hits[0], "rt"))
            else:
                scalefactors = json.load(open(sf_hits[0]))
        except Exception:
            pass
    if images or "spatial" in adata.obsm:
        adata.uns["spatial"] = {gsm: {"images": images, "scalefactors": scalefactors}}

    adata.var["feature_type"] = "Gene Expression"
    adata.var["genome"] = "mm10" if SAMPLE_META.get("species") == "Mus musculus" else "hg38"
    return adata

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
    compute_cell_qc(adata, MITO_PATTERNS.get(species, r"^mt-"))
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
    min_cells = thr.get("min_cells_per_gene", 10)
    if min_cells:
        clean.var["n_cells"] = np.asarray((clean.X > 0).sum(axis=0)).ravel()
        clean = clean[:, clean.var["n_cells"] >= min_cells].copy()
    post_cells, post_genes = clean.n_obs, clean.n_vars
    warn = keep_frac < thr.get("keep_fraction_min", 0.0)
    metrics = {
        "gsm": SAMPLE_META.get("gsm"), "assay": "Visium HD", "species": species,
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

def write_qc_report(gsm: str, metrics: Dict[str, Any], thr: Dict[str, Any],
                    raw_files: list[str], out_txt: Path) -> None:
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
        f"  median genes/cell : {metrics['median_genes_per_unit']:.2f}",
        f"  median counts/cell: {metrics['median_counts_per_unit']:.2f}",
        f"  median mito %     : {metrics['median_pct_mito']:.2f}%",
        "", "  --- Thresholds applied ---",
    ]
    for k, v in thr.items():
        lines.append(f"  {k:<22}: {v}")
    lines.extend([
        "", "  --- Outcome ---",
        f"  QC pass           : {metrics['qc_pass']}",
        f"  Note              : {metrics['qc_note']}",
        bar,
    ])
    out_txt.write_text("\n".join(lines) + "\n")
    log("INFO", f"wrote {out_txt}")

def plot_qc(adata: ad.AnnData, gsm: str, out_png: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    if "spatial" in adata.obsm:
        xy = adata.obsm["spatial"]
        counts = adata.obs["n_counts"].values
        # subsample if > 50,000 cells for plotting speed
        if len(xy) > 50000:
            idx = np.random.choice(len(xy), 50000, replace=False)
            xy = xy[idx]
            counts = counts[idx]
        sc = ax.scatter(xy[:, 0], xy[:, 1], c=counts, cmap="viridis", s=0.5, alpha=0.8)
        fig.colorbar(sc, ax=ax, label="UMI counts")
        ax.set_title(f"{gsm} cell segmentations (UMI counts)")
    else:
        ax.text(0.5, 0.5, "No spatial coordinates", ha="center", va="center")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(str(out_png), dpi=150)
    plt.close(fig)
    log("INFO", f"wrote {out_png}")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=Path("raw"))
    parser.add_argument("--raw-out", type=Path, default=Path("raw"))
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--tmp-dir", type=Path, default=Path("tmp"))
    args = parser.parse_args()

    raw_dir: Path = args.raw_dir
    raw_out: Path = args.raw_out
    data_dir: Path = args.data_dir
    tmp_dir: Path = args.tmp_dir
    gsm = SAMPLE_META["gsm"]

    data_dir.mkdir(parents=True, exist_ok=True)
    raw_out.mkdir(parents=True, exist_ok=True)

    log("INFO", f"process start for {gsm} (Visium HD)")
    adata = read_visiumhd(raw_dir, gsm)
    
    # Pre-QC snapshot
    raw_out_h5 = raw_out / f"{gsm}_raw_counts.h5"
    adata.write_h5ad(str(raw_out_h5))
    log("INFO", f"wrote raw counts (pre-QC) {raw_out_h5} ({adata.n_obs} x {adata.n_vars})")

    # Standardize obs
    obs_df = build_obs(adata.n_obs)
    obs_df.index = adata.obs_names
    adata.obs = obs_df

    metrics, clean = run_qc(adata, SAMPLE_META["species"], THRESHOLDS)
    metrics["gsm"] = gsm

    # Write processed
    proc_h5 = data_dir / f"{gsm}_processed.h5"
    clean.write_h5ad(str(proc_h5))
    log("INFO", f"wrote {proc_h5} ({clean.n_obs} x {clean.n_vars})")

    # Write QC JSON
    proc_qc_json = data_dir / f"{gsm}_processed.qc.json"
    with open(proc_qc_json, "w") as f:
        json.dump(metrics, f, indent=2)
    log("INFO", f"wrote {proc_qc_json}")

    # Write text report
    raw_files = [f.name for f in sorted(raw_dir.iterdir()) if f.is_file() and not f.name.endswith("_raw_counts.h5")]
    qc_txt = data_dir / f"{gsm}_qc_report.txt"
    write_qc_report(gsm, metrics, THRESHOLDS, raw_files, qc_txt)

    # Plot QC
    out_png = data_dir / f"{gsm}_umi_counts.png"
    plot_qc(clean, gsm, out_png)

    log("INFO", f"process done for {gsm}: {metrics['qc_note']}")

if __name__ == "__main__":
    main()
