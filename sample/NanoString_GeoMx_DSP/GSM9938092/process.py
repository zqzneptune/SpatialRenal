#!/usr/bin/env python
"""Per-sample ingestion + QC: raw/ -> data/GSM9938092_processed.h5.

For this single sample
(GSM9938092, kidney allograft; patient 1; DSA+CAMR; glomerulus / —, GeoMx DSP spatial transcriptomics (region-based)), parse the original author-distributed files in
``raw/`` into a standardized, QC-filtered AnnData stored under the unified name
``data/GSM9938092_processed.h5`` (h5ad-compatible HDF5), plus a matching QC report
``data/GSM9938092_processed.qc.json``.

Provenance:
  gsm        : GSM9938092
  study      : CAMR-GeoMx (GSE342778)
  condition  : kidney allograft; patient 1; DSA+CAMR; glomerulus / —
  species    : Homo sapiens
  modality   : spatial (NanoString GeoMx DSP)
  raw files  : GSE342778_Hs_R_NGS_WTA_v1.0.pkc.gz; GSM9938092_DSP-1001660023291-D-D05.dcc.gz

Usage:
    process.py --raw-dir raw --data-dir data --tmp-dir tmp
"""

from __future__ import annotations

import argparse
import datetime as _dt
import gzip
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
import scanpy as sc
import anndata as ad
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
    'gsm': 'GSM9938092',
    'sample_id': 'ROI004 GLM',
    'species': 'Homo sapiens',
    'gse': 'GSE342778',
    'study': 'CAMR-GeoMx',
    'modality': 'spatial',
    'platform': 'NanoString GeoMx DSP',
    'disease_condition': 'transplant-CAMR (GeoMx)',
    'tissue_region': 'glomerulus',
    'sex': 'NA',
    'age': 'NA',
    'treatment': 'NA',
    'model_genotype': 'NA',
    'patient_individual': 'patient 1',
    'panel_probes': 'GeoMx Human NGS WTA (18,677 targets)',
    'prep': 'FFPE',
    'reference_genome': 'hg38',
    'condition_detail': 'kidney allograft; patient 1; DSA+CAMR; glomerulus',
    'timepoint': '—',
}

# Quality control parameters
THRESHOLDS: Dict[str, float] = {
    "min_counts_per_roi": 1000,
    "min_targets_per_roi": 100,
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
# DCC + PKC parsing
# --------------------------------------------------------------------------- #
def parse_dcc(dcc_path: Path) -> Dict[str, int]:
    """Return {RTS_ID: raw count} from a GeoMx DCC ``<Code_Summary>``."""
    raw = gzip.open(dcc_path, "rb").read().decode("latin1", errors="replace")
    m = re.search(r"<Code_Summary>(.*?)</Code_Summary>", raw, re.S)
    if not m:
        log("ERROR", f"no <Code_Summary> in {dcc_path.name}")
        sys.exit(3)
    counts = {}
    for line in m.group(1).strip().splitlines():
        rid, c = line.split(",")
        counts[rid.strip()] = int(c)
    return counts


def parse_pkc(pkc_path: Path) -> Dict[str, str]:
    """Return {RTS_ID: gene} from the shared GeoMx PKC JSON."""
    pkc = json.load(gzip.open(pkc_path, "rt"))
    rts2gene = {}
    for t in pkc.get("Targets", []):
        for pr in t.get("Probes", []):
            rid = pr.get("RTS_ID")
            if not rid:
                continue
            g = pr.get("SystematicName")
            if isinstance(g, list):
                g = g[0] if g else None
            if not g:
                g = pr.get("DisplayName")
            if g:
                rts2gene[rid] = g
    log("INFO", f"parsed {len(rts2gene)} RTS->gene entries from {pkc_path.name}")
    return rts2gene


def read_geomx(raw_dir: Path, gsm: str) -> ad.AnnData:
    dccs = sorted(raw_dir.glob(f"{gsm}*.dcc.gz"))
    if not dccs:
        log("ERROR", f"no dcc.gz for {gsm} under {raw_dir}")
        sys.exit(3)
    pkcs = sorted(raw_dir.glob("*.pkc.gz"))
    if not pkcs:
        log("ERROR", f"no pkc.gz under {raw_dir}")
        sys.exit(3)
    counts = parse_dcc(dccs[0])
    rts2gene = parse_pkc(pkcs[0])

    gene_counts: Dict[str, int] = {}
    unmapped = 0
    for rid, c in counts.items():
        g = rts2gene.get(rid)
        if g:
            gene_counts[g] = gene_counts.get(g, 0) + c
        else:
            unmapped += 1
    if unmapped:
        log("WARN", f"{unmapped} RTS codes had no gene mapping")

    genes = sorted(gene_counts)
    X = np.array([[gene_counts[g] for g in genes]], dtype=np.float32)
    adata = ad.AnnData(X=X, var=pd.DataFrame(index=genes))
    adata.var["feature_type"] = "Gene Expression"
    adata.var["genome"] = "hg38" if SAMPLE_META.get("species") == "Homo sapiens" else "mm10"
    log("INFO", f"built GeoMx ROI matrix ({adata.n_obs} ROI x {adata.n_vars} genes, {int(X.sum())} counts)")
    return adata


# --------------------------------------------------------------------------- #
# QC
# --------------------------------------------------------------------------- #
MITO_PATTERNS = {"Homo sapiens": r"^MT-", "Mus musculus": r"^mt-"}


def compute_roi_qc(adata: ad.AnnData, mito_pat: str) -> ad.AnnData:
    mito = adata.var_names.str.contains(mito_pat, regex=True, na=False)
    adata.obs["n_genes"] = np.asarray((adata.X > 0).sum(axis=1)).ravel()
    adata.obs["n_counts"] = np.asarray(adata.X.sum(axis=1)).ravel()
    if mito.any():
        mito_counts = np.asarray(adata[:, mito].X.sum(axis=1)).ravel()
        adata.obs["pct_mito"] = 100.0 * mito_counts / np.maximum(adata.obs["n_counts"].values, 1)
    else:
        adata.obs["pct_mito"] = 0.0
    return adata


def run_qc(adata: ad.AnnData, thr: Dict[str, Any]) -> Tuple[Dict[str, Any], ad.AnnData]:
    pre_cells = adata.n_obs  # 1 ROI
    pre_genes = adata.n_vars
    compute_roi_qc(adata, MITO_PATTERNS.get(SAMPLE_META.get("species", ""), r"^MT-"))
    total = int(adata.obs["n_counts"].iloc[0])
    n_targets = int(adata.obs["n_genes"].iloc[0])
    ok = total >= thr.get("min_counts_per_roi", 0) and n_targets >= thr.get("min_targets_per_roi", 0)
    adata.obs["qc_pass"] = True
    keep_frac = 1.0
    metrics = {
        "gsm": None, "assay": "GeoMx", "species": SAMPLE_META.get("species", "NA"),
        "pre_cells": pre_cells, "pre_genes": pre_genes,
        "post_cells": pre_cells, "post_genes": pre_genes,
        "keep_fraction": 1.0,
        "median_genes_per_unit": float(n_targets),
        "median_counts_per_unit": float(total),
        "median_pct_mito": float(adata.obs["pct_mito"].iloc[0]),
        "qc_pass": ok,
        "qc_note": (f"ROI: {total} counts / {n_targets} targets (thresholds: "
                    f">={thr.get('min_counts_per_roi', 0)} counts, "
                    f">={thr.get('min_targets_per_roi', 0)} targets)"
                    + ("" if ok else "; WARN below GeoMx thresholds")),
    }
    return metrics, adata


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
        bar, f"  QC REPORT — {gsm}  (GeoMx DSP, single ROI)", bar,
        f"  Study             : {meta.get('study', 'NA')} ({meta.get('gse', 'NA')})",
        f"  Condition         : {meta.get('condition_detail', 'NA')} / {meta.get('timepoint', 'NA')}",
        f"  Species           : {meta.get('species', 'NA')}",
        f"  Assay / Platform  : {metrics['assay']} / {meta.get('platform', 'NA')}",
        f"  Region            : {meta.get('tissue_region', 'NA')}",
        f"  Source (raw/)     : {', '.join(raw_files) or 'NA'}",
        "", "  --- Counts ---",
        f"  ROI total counts  : {metrics['median_counts_per_unit']:.0f}",
        f"  targets (genes)   : {metrics['median_genes_per_unit']:.0f}",
        f"  % mito            : {fmt(metrics['median_pct_mito'])}",
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
    """GeoMx has no spatial image/coordinates -> top-gene counts barplot."""
    n_counts = np.asarray(adata.X.sum(axis=0)).ravel()
    order = np.argsort(n_counts)[::-1][:20]
    top = adata.var_names[order][::-1]
    vals = n_counts[order][::-1]
    fig, ax = plt.subplots(1, 1, figsize=(7, 6))
    ax.barh(np.arange(len(vals)), vals, color="steelblue")
    ax.set_yticks(np.arange(len(vals))); ax.set_yticklabels(top)
    ax.set_xlabel("raw counts"); ax.set_title(f"{gsm} — top genes (GeoMx ROI)")
    fig.tight_layout(); fig.savefig(str(out_png), dpi=200, bbox_inches="tight"); plt.close(fig)
    log("INFO", f"wrote {out_png} (GeoMx top-gene barplot)")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--gsm", default=SAMPLE_META["gsm"], help="GEO sample accession")
    p.add_argument("--raw-dir", default="raw", help="read-only original files (dcc.gz + pkc.gz)")
    p.add_argument("--raw-out", default="raw", help="output directory for pre-QC counts file")
    p.add_argument("--data-dir", default="data", help="output dir for processed.h5 / qc.* / figure")
    p.add_argument("--tmp-dir", default="tmp", help="temporary working directory")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    gsm = SAMPLE_META["gsm"]
    log("INFO", f"process start for {gsm} (GeoMx dcc)")

    raw_dir = Path(args.raw_dir)
    raw_out = Path(args.raw_out)
    data_dir = Path(args.data_dir)
    tmp_dir = Path(args.tmp_dir)
    raw_out.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    raw_files = [p.name for p in raw_dir.iterdir()
                 if p.is_file() and not p.name.endswith("_raw_counts.h5")]
    adata = read_geomx(raw_dir, gsm)

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
        "script": "process.py (geomx_dcc variant)",
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
