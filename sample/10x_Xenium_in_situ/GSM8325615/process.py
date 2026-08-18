#!/usr/bin/env python
"""Per-sample ingestion + QC: raw/ -> data/GSM8325615_processed.h5.

For this single sample
(GSM8325615, bIRI sham / sham L, Xenium in situ spatial transcriptomics), parse the original author-distributed files in
``raw/`` into a standardized, QC-filtered AnnData stored under the unified name
``data/GSM8325615_processed.h5`` (h5ad-compatible HDF5), plus a matching QC report
``data/GSM8325615_processed.qc.json``.

Provenance:
  gsm        : GSM8325615
  study      : mouse-IRI-repair (GSE269884; Nat Commun s41467-025-62599-9)
  condition  : bIRI sham / sham L
  species    : Mus musculus
  modality   : spatial (10x Xenium in situ)
  raw files  : GSM8325615_xenium_shamL_male_baysor_segmentation.tar.gz; GSM8325615_xenium_shamL_male_output.tar.gz

Usage:
    process.py --raw-dir raw --data-dir data --tmp-dir tmp
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import re
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
import tifffile


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
    'gsm': 'GSM8325615',
    'sample_id': 'xenium_shamL',
    'species': 'Mus musculus',
    'gse': 'GSE269884',
    'study': 'mouse-IRI-repair',
    'modality': 'spatial',
    'platform': '10x Xenium in situ',
    'disease_condition': 'sham (control)',
    'tissue_region': 'whole kidney',
    'sex': 'male',
    'age': '8-10 weeks',
    'treatment': 'NA',
    'model_genotype': 'C57BL/6J',
    'patient_individual': 'mouse:sham',
    'panel_probes': 'Xenium 300 genes',
    'prep': 'FFPE',
    'reference_genome': 'mm10-2020-A',
    'condition_detail': 'bIRI sham',
    'timepoint': 'sham L',
}

# Quality control parameters
THRESHOLDS: Dict[str, float] = {
    "min_transcripts_per_cell": 10,
    "min_genes_per_cell": 3,
    "min_cells_per_gene": 10,
    "keep_fraction_min": 0.50,
}


# --------------------------------------------------------------------------- #
# obs table from embedded metadata
# --------------------------------------------------------------------------- #
def build_obs(n_units: int) -> pd.DataFrame:
    """Build the standardized per-cell obs table from the embedded SAMPLE_META."""
    meta: Dict[str, Any] = dict(SAMPLE_META)
    for c in ("n_genes", "n_counts", "pct_mito", "qc_pass"):
        meta[c] = np.nan
    return pd.DataFrame([meta] * n_units)


# --------------------------------------------------------------------------- #
# Xenium staging + reading (standard output)
# --------------------------------------------------------------------------- #
def stage_xenium(data_dir: Path, gsm: str, tmp_dir: Path) -> Tuple[Path, Path, Optional[Path], Optional[Path]]:
    """Extract Xenium essentials + morphology image from ``*_output.tar.gz``.

    Returns ``(matrix_dir, cells_csv, panel_json, morph_tif)`` — the
    ``cell_feature_matrix/``, ``cells.csv.gz``, ``gene_panel.json`` and the
    ``morphology_focus.ome.tif`` (fluorescence image) for the UMI overlay.
    """
    tars = [p for p in sorted(data_dir.glob(f"{gsm}*"))
            if p.suffix == ".gz" and "output" in p.name]
    if not tars:
        log("ERROR", f"no Xenium output tar for {gsm} under {data_dir}")
        sys.exit(3)
    stage = tmp_dir / f"{gsm}_xenium"
    found = False
    for tar in tars:
        try:
            with tarfile.open(tar, "r:*") as tf:
                members = [
                    m for m in tf.getmembers()
                    if m.isfile() and not m.name.startswith("._") and (
                        "cell_feature_matrix/" in m.name
                        or m.name.endswith(("cells.csv.gz", "gene_panel.json",
                                            "metrics_summary.csv", "morphology_focus.ome.tif"))
                    )
                ]
                if not members:
                    continue
                for m in members:
                    tf.extract(m, path=stage, filter="data")
                found = True
                log("INFO", f"extracted Xenium essentials for {gsm} ({len(members)} files)")
                break
        except (tarfile.TarError, OSError) as e:
            log("WARN", f"tar {tar} not readable: {e}")
    if not found:
        log("ERROR", f"no cell_feature_matrix found in Xenium tars for {gsm}")
        sys.exit(3)

    matrix_dir = next(stage.rglob("cell_feature_matrix"), None)
    cells_csv = next(stage.rglob("cells.csv.gz"), None)
    panel_json = next(stage.rglob("gene_panel.json"), None)
    morph_tif = next(stage.rglob("morphology_focus.ome.tif"), None)
    if matrix_dir is None or cells_csv is None:
        log("ERROR", f"missing cell_feature_matrix or cells.csv.gz for {gsm}")
        sys.exit(3)
    return matrix_dir, cells_csv, panel_json, morph_tif


def read_xenium(matrix_dir: Path, cells_csv: Path, species: str,
                panel_json: Optional[Path] = None) -> ad.AnnData:
    """Assemble a Xenium AnnData from the standard output matrix + centroids."""
    adata = sc.read_10x_mtx(str(matrix_dir), var_names="gene_symbols", make_unique=True, gex_only=True)

    cells = pd.read_csv(cells_csv)
    cells = cells.set_index("cell_id").reindex(adata.obs_names)
    for c in ("transcript_counts", "total_counts", "cell_area", "nucleus_area"):
        if c in cells.columns:
            adata.obs[c] = cells[c].values
    if "x_centroid" in cells.columns and "y_centroid" in cells.columns:
        adata.obsm["spatial"] = cells[["x_centroid", "y_centroid"]].values.astype(float)

    if panel_json is not None and panel_json.exists():
        try:
            panel = json.load(open(panel_json))
            payload = panel.get("payload", panel)
            info: Dict[str, Any] = {"panel_name": None, "n_targets": 0, "n_genes": 0, "gene_list": []}
            pobj = payload.get("panel")
            if isinstance(pobj, dict):
                info["panel_name"] = pobj.get("name")
            elif isinstance(pobj, str):
                info["panel_name"] = pobj
            targets = payload.get("targets", [])
            if isinstance(targets, list):
                info["n_targets"] = len(targets)
                genes = [t.get("type", {}).get("data", {}).get("name")
                         for t in targets if isinstance(t, dict)
                         and t.get("type", {}).get("descriptor") == "gene"]
                info["gene_list"] = [g for g in genes if g]
                info["n_genes"] = len(info["gene_list"])
            adata.uns["xenium"] = info
        except (OSError, json.JSONDecodeError, AttributeError) as e:
            log("WARN", f"could not parse gene_panel.json: {e}")

    adata.var["feature_type"] = "Gene Expression"
    adata.var["genome"] = "hg38" if species == "Homo sapiens" else "mm10"
    return adata


# --------------------------------------------------------------------------- #
# QC
# --------------------------------------------------------------------------- #
MITO_PATTERNS = {"Homo sapiens": r"^MT-", "Mus musculus": r"^mt-"}


def compute_cell_qc(adata: ad.AnnData, mito_pat: str) -> ad.AnnData:
    """Add n_genes / n_counts / pct_mito to obs (raw counts required)."""
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
    """Filter cells/genes with Xenium thresholds; return (metrics, filtered_adata)."""
    pre_cells = adata.n_obs
    pre_genes = adata.n_vars

    compute_cell_qc(adata, MITO_PATTERNS.get(species, r"^MT-"))

    mask = pd.Series(True, index=adata.obs_names)
    if "min_genes_per_cell" in thr:
        mask &= adata.obs["n_genes"] >= thr["min_genes_per_cell"]
    if "min_counts_per_cell" in thr:
        mask &= adata.obs["n_counts"] >= thr["min_counts_per_cell"]
    if "min_transcripts_per_cell" in thr:
        mask &= adata.obs["n_counts"] >= thr["min_transcripts_per_cell"]
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

    post_cells = clean.n_obs
    post_genes = clean.n_vars
    warn = keep_frac < thr.get("keep_fraction_min", 0.0)

    metrics = {
        "gsm": None, "assay": "Xenium", "species": species,
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
# Outputs: QC text report + UMI overlay figure
# --------------------------------------------------------------------------- #
def fmt(x: Any) -> str:
    try:
        return f"{float(x):.2f}" if np.isfinite(float(x)) else "n/a"
    except (TypeError, ValueError):
        return str(x)


def write_qc_report(gsm: str, metrics: Dict[str, Any], thr: Dict[str, Any],
                    raw_files: "list[str]", out_txt: Path) -> None:
    """Write a human-readable QC report (data/GSMxxxxx_qc_report.txt)."""
    meta = SAMPLE_META
    bar = "=" * 78
    lines = [
        bar,
        f"  QC REPORT — {gsm}",
        bar,
        f"  Study             : {meta.get('study', 'NA')} ({meta.get('gse', 'NA')})",
        f"  Condition         : {meta.get('condition_detail', 'NA')} / {meta.get('timepoint', 'NA')}",
        f"  Species           : {meta.get('species', 'NA')}",
        f"  Assay / Platform  : {metrics['assay']} / {meta.get('platform', 'NA')}",
        f"  Source (raw/)     : {', '.join(raw_files) or 'NA'}",
        "",
        "  --- Pre-QC ---",
        f"  units             : {metrics['pre_cells']}",
        f"  genes             : {metrics['pre_genes']}",
        "",
        "  --- Post-QC (filtered) ---",
        f"  units             : {metrics['post_cells']}   (kept {metrics['keep_fraction']:.1%})",
        f"  genes             : {metrics['post_genes']}",
        f"  median genes/unit : {fmt(metrics['median_genes_per_unit'])}",
        f"  median counts/unit: {fmt(metrics['median_counts_per_unit'])}",
        f"  median % mito     : {fmt(metrics['median_pct_mito'])}",
        "",
        "  --- Thresholds applied ---",
    ]
    lines += [f"  {k:<24}: {v}" for k, v in thr.items()]
    lines += [
        "",
        f"  QC result         : {'PASS' if metrics['qc_pass'] else 'WARN'}",
        f"  Note              : {metrics['qc_note']}",
        "",
        f"  Outputs : data/{gsm}_processed.h5 · data/{gsm}_processed.qc.json · data/{gsm}_umi_counts.png",
        f"  Raw counts (pre-QC) : raw/{gsm}_raw_counts.h5",
        f"  Generated : {_dt.datetime.now().isoformat()}  (process.py)",
        bar,
    ]
    out_txt.write_text("\n".join(lines) + "\n")
    log("INFO", f"wrote {out_txt}")


def plot_umi_overlay(adata: ad.AnnData, gsm: str, out_png: Path, morph_tif: Optional[Path]) -> None:
    """UMI counts per cell overlaid on the fluorescence (morphology_focus) image.

    Cell centroids (``obsm['spatial']``, µm) are mapped to image pixels via the
    OME physical pixel size, then scaled by the pyramid-level downsampling
    factor so a full-resolution OME-TIFF is never loaded into memory.
    """
    if morph_tif is None or not morph_tif.exists():
        log("WARN", f"no morphology_focus.ome.tif for {gsm}; plotting centroids on plain background")
        fig, ax = plt.subplots(1, 1, figsize=(9, 9))
        scatter = ax.scatter(adata.obsm["spatial"][:, 0], adata.obsm["spatial"][:, 1],
                             c=np.log1p(adata.obs["n_counts"]), cmap="magma", s=0.6, alpha=0.7)
        plt.colorbar(scatter, ax=ax, label="log1p(UMI counts)")
        ax.set_title(f"{gsm} — UMI counts per cell")
        ax.set_aspect("equal"); ax.axis("off")
        fig.savefig(str(out_png), dpi=200, bbox_inches="tight")
        plt.close(fig)
        log("INFO", f"wrote {out_png} (no-image fallback)")
        return

    tif = tifffile.TiffFile(str(morph_tif))
    s = tif.series[0]
    w = s.shape[-1]
    k = min(len(s.levels) - 1, max(0, round(math.log2(max(1, w / 3000)))))
    img = s.levels[k].asarray()
    if img.ndim == 3:
        img = img[0]
    scale = 2 ** k

    xml = s.pages[0].tags.get(270).value
    m = re.search(r'PhysicalSizeX="([\d.]+)"', xml)
    pixel_size = float(m.group(1)) if m else 0.2125

    px = adata.obsm["spatial"][:, 0] / pixel_size / scale
    py = adata.obsm["spatial"][:, 1] / pixel_size / scale

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    vmin, vmax = np.percentile(img, (1, 99))
    ax.imshow(img, cmap="gray", vmin=float(vmin), vmax=float(vmax))
    scatter = ax.scatter(px, py, c=np.log1p(adata.obs["n_counts"]), cmap="magma",
                         s=0.5, alpha=0.7, rasterized=True)
    plt.colorbar(scatter, ax=ax, label="log1p(UMI counts)")
    ax.set_title(f"{gsm} — UMI counts per cell")
    ax.axis("off")
    fig.savefig(str(out_png), dpi=200, bbox_inches="tight")
    plt.close(fig)
    log("INFO", f"wrote {out_png} (image overlay, level {k}, pixel {pixel_size} µm)")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--gsm", default=SAMPLE_META["gsm"], help="GEO sample accession (defaults to SAMPLE_META)")
    p.add_argument("--raw-dir", default="raw", help="read-only original files (Xenium output tar)")
    p.add_argument("--raw-out", default="raw", help="output directory for pre-QC counts file")
    p.add_argument("--data-dir", default="data", help="output dir for processed.h5 / qc.* / umi figure")
    p.add_argument("--tmp-dir", default="tmp", help="temporary working directory")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    gsm = SAMPLE_META["gsm"]
    log("INFO", f"process start for {gsm} (Xenium)")

    raw_dir = Path(args.raw_dir)
    raw_out = Path(args.raw_out)
    data_dir = Path(args.data_dir)
    tmp_dir = Path(args.tmp_dir)
    raw_out.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    raw_files = [p.name for p in raw_dir.iterdir()
                 if p.is_file() and not p.name.endswith("_raw_counts.h5")]
    matrix_dir, cells_csv, panel_json, morph_tif = stage_xenium(raw_dir, gsm, tmp_dir)
    adata = read_xenium(matrix_dir, cells_csv, SAMPLE_META.get("species", "NA"), panel_json)

    # 1) Pre-QC raw counts export -> raw/ (counts + coordinates only)
    raw_counts_adata = adata.copy()
    raw_counts_adata.uns.pop("spatial", None)
    raw_counts_adata.write_h5ad(str(raw_out / f"{gsm}_raw_counts.h5"))
    log("INFO", f"wrote raw counts (pre-QC) {raw_out / f'{gsm}_raw_counts.h5'} ({raw_counts_adata.n_obs} x {raw_counts_adata.n_vars})")

    # 2) QC
    species = SAMPLE_META.get("species", "NA")
    metrics, clean = run_qc(adata, species, THRESHOLDS)

    # 3) standardized obs
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
        "script": "process.py (xenium variant)",
        "thresholds": THRESHOLDS,
        "metadata_source": "SAMPLE_META",
        "timestamp": _dt.datetime.now().isoformat(),
    }

    # 4) outputs
    out_h5 = data_dir / f"{gsm}_processed.h5"
    clean.write_h5ad(str(out_h5))
    log("INFO", f"wrote {out_h5} ({clean.n_obs} x {clean.n_vars})")

    metrics["gsm"] = gsm
    out_qc = data_dir / f"{gsm}_processed.qc.json"
    with open(out_qc, "w") as f:
        json.dump(metrics, f, indent=2)
    log("INFO", f"wrote {out_qc}")

    write_qc_report(gsm, metrics, THRESHOLDS, raw_files, data_dir / f"{gsm}_qc_report.txt")
    plot_umi_overlay(clean, gsm, data_dir / f"{gsm}_umi_counts.png", morph_tif)

    log("INFO", f"process done for {gsm}: {metrics['qc_note']}")


if __name__ == "__main__":
    main()
