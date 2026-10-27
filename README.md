# SpatialRenal

> Standardized preprocessing and quality control (QC) Python pipelines for kidney spatial transcriptomics and spatial omics datasets.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Scanpy](https://img.shields.io/badge/Scanpy-v1.10+-brightgreen.svg)](https://scanpy.readthedocs.io/)
[![Spatial Omics](https://img.shields.io/badge/Spatial%20Omics-197%20Samples-orange.svg)]()

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Python Environment Setup](#2-python-environment-setup)
  - [Option A: Conda / Mamba Environment (Recommended)](#option-a-conda--mamba-environment-recommended)
  - [Option B: Pip Installation](#option-b-pip-installation)
  - [Verification](#verification)
- [3. Repository Architecture & Usage](#3-repository-architecture--usage)
  - [How to Process a Sample](#how-to-process-a-sample)
- [4. Sample Catalog](#4-sample-catalog)
  - [4.1 10x Genomics Visium (64 Samples)](#41-10x-genomics-visium-64-samples)
  - [4.2 10x Genomics Visium CytAssist (14 Samples)](#42-10x-genomics-visium-cytassist-14-samples)
  - [4.3 10x Genomics Visium HD (12 Samples)](#43-10x-genomics-visium-hd-12-samples)
  - [4.4 10x Genomics Xenium in situ (56 Samples)](#44-10x-genomics-xenium-in-situ-56-samples)
  - [4.5 NanoString CosMx SMI (3 Samples)](#45-nanostring-cosmx-smi-3-samples)
  - [4.6 NanoString GeoMx DSP (48 Samples)](#46-nanostring-geomx-dsp-48-samples)
- [5. Platform Summary](#5-platform-summary)
- [6. Disclaimer & Attribution](#6-disclaimer--attribution)
- [7. License](#7-license)

---

## 1. Overview

**SpatialRenal** is a curated repository hosting reproducible, per-sample preprocessing and quality control (QC) Python scripts for published kidney spatial transcriptomics datasets.

- **197 Spatial Samples**: Covering **27 studies** across human and mouse kidney models.
- **6 Spatial Platforms Supported**:
  - **10x Genomics Visium** (64 samples)
  - **10x Genomics Visium CytAssist** (14 samples)
  - **10x Genomics Visium HD** (12 samples)
  - **10x Genomics Xenium in situ** (56 samples)
  - **NanoString CosMx SMI** (3 samples)
  - **NanoString GeoMx DSP** (48 samples)
- **Code & Metadata Only**: To ensure lightweight versioning and open access, this repository contains **only Python processing scripts and provenance documentation** — no compiled files, binary datasets, or raw sequencing archives are stored directly in this repository.
- **Standardized Sample Units**: Each sample directory under [`sample/`](sample/) is standalone, embedding the sample's biological metadata and platform-calibrated QC threshold parameters.

---

## 2. Python Environment Setup

The sample preprocessing pipelines rely on standard Python spatial transcriptomics and scientific computing libraries. Python **3.10**, **3.11**, or **3.12** is recommended.

### Option A: Conda / Mamba Environment (Recommended)

```bash
# 1. Create a dedicated conda environment
conda create -n spatialrenal python=3.12 -y

# 2. Activate the environment
conda activate spatialrenal

# 3. Install core spatial transcriptomics dependencies from conda-forge
conda install -c conda-forge -y \
    anndata \
    scanpy \
    numpy \
    pandas \
    scipy \
    matplotlib \
    pillow \
    tifffile \
    zarr \
    h5py
```

### Option B: Pip Installation

```bash
# Create and activate virtual environment
python3 -m venv spatialrenal_env
source spatialrenal_env/bin/activate

# Install required packages
pip install --upgrade pip
pip install \
    "scanpy>=1.10.0" \
    "anndata>=0.10.0" \
    "numpy>=1.24.0" \
    "pandas>=2.0.0" \
    "scipy>=1.10.0" \
    "matplotlib>=3.8.0" \
    "pillow>=10.0.0" \
    "tifffile>=2024.0.0" \
    "zarr>=2.16.0" \
    "h5py>=3.10.0"
```

### Verification

Verify that all necessary packages are properly installed:

```bash
python -c "import scanpy, anndata, numpy, pandas, scipy, matplotlib, PIL, tifffile, zarr, h5py; print('✓ SpatialRenal environment is ready!')"
```

---

## 3. Repository Architecture & Usage

The repository is organized by platform, where each sample lives in its own directory:

```
SpatialRenal/
├── LICENSE                                # MIT License
├── README.md                              # Main registry & documentation
└── sample/
    ├── 10x_Visium/                        # 10x Genomics Visium samples
    │   └── GSMxxxxxxx/
    │       ├── README.md                  # Sample metadata, raw file requirements, and GEO links
    │       └── process.py                 # Preprocessing & QC pipeline
    ├── 10x_Visium_CytAssist/              # 10x Genomics Visium CytAssist samples
    ├── 10x_Visium_HD/                     # 10x Genomics Visium HD samples
    ├── 10x_Xenium_in_situ/                # 10x Genomics Xenium in situ samples
    ├── NanoString_CosMx_SMI/              # NanoString CosMx SMI samples
    └── NanoString_GeoMx_DSP/              # NanoString GeoMx DSP samples
```

### How to Process a Sample

1. **Locate the sample**: Find your sample of interest in the [Sample Catalog](#4-sample-catalog) below and navigate into its directory.
2. **Review raw file requirements**: Open the sample's `README.md` to see the expected author-distributed raw files and direct GEO download links.
3. **Acquire raw files**: Download the raw files from GEO and place them inside a local `raw/` subdirectory within the sample folder.
4. **Execute processing**:
   ```bash
   cd sample/<Platform>/<GSM>
   mkdir -p raw data tmp
   # (Place downloaded raw files into raw/)
   python process.py --raw-dir raw --data-dir data --tmp-dir tmp
   ```
5. **Outputs produced**:
   - `raw/<GSM>_raw_counts.h5`: Unfiltered raw count matrix (AnnData-compatible HDF5 with coordinates).
   - `data/<GSM>_processed.h5`: QC-filtered and metadata-annotated AnnData object.
   - `data/<GSM>_processed.qc.json`: Standardized QC metrics summary (JSON).
   - `data/<GSM>_qc_report.txt`: Human-readable QC log.
   - `data/<GSM>_umi_counts.png`: High-resolution spatial UMI count visualization.

---

## 4. Sample Catalog

### 4.1 10x Genomics Visium (64 Samples)

| GSM Accession | Sample ID | Species | Study / Series | Disease Condition / Context | Pipeline Link |
|---|---|---|---|---|---|
| [GSM6047778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM6047778) | V10S15-102_XY03_IU-21-015-2 | *Homo sapiens* | kidney-PT-regen ([GSE298953](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE298953)) | reference (nephrectomy control) (reference kidney; reused from GSE183456) | [`GSM6047778`](sample/10x_Visium/GSM6047778/) |
| [GSM6047779](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM6047779) | V10S15-102_XY02_IU-21-019-5 | *Homo sapiens* | kidney-PT-regen ([GSE298953](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE298953)) | reference (nephrectomy control) (reference kidney; reused from GSE183456) | [`GSM6047779`](sample/10x_Visium/GSM6047779/) |
| [GSM8110784](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8110784) | Hyperuricemia mice1 | *Mus musculus* | hyperuricemia-mouse ([GSE258959](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE258959)) | hyperuricemia (Uox-KO) (Uox-KO (hyperuricemia), male, C57BL/6J) | [`GSM8110784`](sample/10x_Visium/GSM8110784/) |
| [GSM8110785](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8110785) | Hyperuricemia mice2 | *Mus musculus* | hyperuricemia-mouse ([GSE258959](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE258959)) | hyperuricemia (Uox-KO) (Uox-KO (hyperuricemia), male, C57BL/6J) | [`GSM8110785`](sample/10x_Visium/GSM8110785/) |
| [GSM8110786](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8110786) | Control mice1 | *Mus musculus* | hyperuricemia-mouse ([GSE258959](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE258959)) | control (control, male, C57BL/6J) | [`GSM8110786`](sample/10x_Visium/GSM8110786/) |
| [GSM8110787](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8110787) | Control mice2 | *Mus musculus* | hyperuricemia-mouse ([GSE258959](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE258959)) | control (control, male, C57BL/6J) | [`GSM8110787`](sample/10x_Visium/GSM8110787/) |
| [GSM9026963](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9026963) | IU-21-019-2 | *Homo sapiens* | kidney-PT-regen ([GSE298953](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE298953)) | reference (nephrectomy control) (reference kidney; nephrectomy) | [`GSM9026963`](sample/10x_Visium/GSM9026963/) |
| [GSM9045323](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9045323) | WT and KO | *Mus musculus* | kidney-repair-matrix ([GSE299736](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299736)) | AKI repair (AKI repair; pooled WT+KO) | [`GSM9045323`](sample/10x_Visium/GSM9045323/) |
| [GSM9108683](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9108683) | ctrl | *Homo sapiens* | ANCA-vasculitis ([GSE302677](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE302677)) | control (kidney cortex, control) | [`GSM9108683`](sample/10x_Visium/GSM9108683/) |
| [GSM9108684](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9108684) | aav1 (mild AAV) | *Homo sapiens* | ANCA-vasculitis ([GSE302677](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE302677)) | ANCA-AAV (mild) (kidney cortex, mild AAV) | [`GSM9108684`](sample/10x_Visium/GSM9108684/) |
| [GSM9108685](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9108685) | aav2 (severe AAV) | *Homo sapiens* | ANCA-vasculitis ([GSE302677](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE302677)) | ANCA-AAV (severe) (kidney cortex, severe AAV) | [`GSM9108685`](sample/10x_Visium/GSM9108685/) |
| [GSM9231917](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231917) | V10S15-103_XY01_IU-21-015F | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; nephrectomy) | [`GSM9231917`](sample/10x_Visium/GSM9231917/) |
| [GSM9231918](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231918) | V10S15-103_XY03_IU-21-019F | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; nephrectomy) | [`GSM9231918`](sample/10x_Visium/GSM9231918/) |
| [GSM9231919](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231919) | V42N07-395_XY04_IU94 | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; biopsy) | [`GSM9231919`](sample/10x_Visium/GSM9231919/) |
| [GSM9231920](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231920) | V42D20-364_XY04_IU92 | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; biopsy) | [`GSM9231920`](sample/10x_Visium/GSM9231920/) |
| [GSM9231921](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231921) | V42N07-395_XY01_IU98 | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; biopsy) | [`GSM9231921`](sample/10x_Visium/GSM9231921/) |
| [GSM9231922](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231922) | V42D20-364_XY01_IU103 | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; biopsy) | [`GSM9231922`](sample/10x_Visium/GSM9231922/) |
| [GSM9231923](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231923) | V42N07-339_XY04_F44 | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; nephrectomy) | [`GSM9231923`](sample/10x_Visium/GSM9231923/) |
| [GSM9231924](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231924) | V10S15-103_XY02_IU-21-016F | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; nephrectomy) | [`GSM9231924`](sample/10x_Visium/GSM9231924/) |
| [GSM9231925](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231925) | V10S15-103_XY04_IU-21-020F | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; nephrectomy) | [`GSM9231925`](sample/10x_Visium/GSM9231925/) |
| [GSM9231926](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231926) | V42N07-339_XY01_3781 | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; nephrectomy) | [`GSM9231926`](sample/10x_Visium/GSM9231926/) |
| [GSM9231927](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231927) | V42N07-399_XY01_3723 | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; nephrectomy) | [`GSM9231927`](sample/10x_Visium/GSM9231927/) |
| [GSM9231928](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231928) | V42N07-399_XY04_3775 | *Homo sapiens* | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) | DKD (diabetic kidney disease; nephrectomy) | [`GSM9231928`](sample/10x_Visium/GSM9231928/) |
| [GSM9247127](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247127) | UUO 7d ligated SK3747 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (UUO 7d, ligated, roxadustat) | [`GSM9247127`](sample/10x_Visium/GSM9247127/) |
| [GSM9247128](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247128) | UUO 7d ligated SK3753 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (UUO 7d, ligated, roxadustat) | [`GSM9247128`](sample/10x_Visium/GSM9247128/) |
| [GSM9247129](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247129) | UUO 7d contralat SK3747 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (UUO 7d, contralateral, roxadustat) | [`GSM9247129`](sample/10x_Visium/GSM9247129/) |
| [GSM9247130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247130) | UUO 7d contralat SK3753 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (UUO 7d, contralateral, roxadustat) | [`GSM9247130`](sample/10x_Visium/GSM9247130/) |
| [GSM9247131](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247131) | healthy roxadustat SK7543 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (healthy, roxadustat) | [`GSM9247131`](sample/10x_Visium/GSM9247131/) |
| [GSM9247132](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247132) | healthy roxadustat SK9682 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (healthy, roxadustat) | [`GSM9247132`](sample/10x_Visium/GSM9247132/) |
| [GSM9247133](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247133) | healthy hypoxia SK4156 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (healthy, hypoxia (0.1% CO)) | [`GSM9247133`](sample/10x_Visium/GSM9247133/) |
| [GSM9247134](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247134) | healthy hypoxia SO4157 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (healthy, hypoxia (0.1% CO)) | [`GSM9247134`](sample/10x_Visium/GSM9247134/) |
| [GSM9247135](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247135) | healthy normoxia SM1758 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (healthy, tamoxifen ctrl (normoxia)) | [`GSM9247135`](sample/10x_Visium/GSM9247135/) |
| [GSM9247136](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247136) | healthy normoxia SM1763 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (healthy, tamoxifen ctrl (normoxia)) | [`GSM9247136`](sample/10x_Visium/GSM9247136/) |
| [GSM9247137](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247137) | UUO 3d ligated SK1441 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (UUO 3d, ligated) | [`GSM9247137`](sample/10x_Visium/GSM9247137/) |
| [GSM9247138](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247138) | UUO 3d ligated SK1440 | *Mus musculus* | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) | EPO/hypoxia model (UUO 3d, ligated) | [`GSM9247138`](sample/10x_Visium/GSM9247138/) |
| [GSM9579055](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9579055) | NZB/WF1 30w rep1 | *Mus musculus* | lupus-nephritis-mouse ([GSE322686](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE322686)) | lupus nephritis (lupus nephritis, NZB/WF1 F1 female, 30 weeks) | [`GSM9579055`](sample/10x_Visium/GSM9579055/) |
| [GSM9579056](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9579056) | NZB/WF1 30w rep2 | *Mus musculus* | lupus-nephritis-mouse ([GSE322686](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE322686)) | lupus nephritis (lupus nephritis, NZB/WF1 F1 female, 30 weeks) | [`GSM9579056`](sample/10x_Visium/GSM9579056/) |
| [GSM9579057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9579057) | NZB/WF1 30w rep3 | *Mus musculus* | lupus-nephritis-mouse ([GSE322686](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE322686)) | lupus nephritis (lupus nephritis, NZB/WF1 F1 female, 30 weeks) | [`GSM9579057`](sample/10x_Visium/GSM9579057/) |
| [GSM9579058](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9579058) | NZB/WF1 30w rep4 | *Mus musculus* | lupus-nephritis-mouse ([GSE322686](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE322686)) | lupus nephritis (lupus nephritis, NZB/WF1 F1 female, 30 weeks) | [`GSM9579058`](sample/10x_Visium/GSM9579058/) |
| [GSM9566413](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9566413) | Kidney_Control | *Mus musculus* | kidney-alcohol-injury ([GSE323994](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE323994)) | control (Control (liquid diet)) | [`GSM9566413`](sample/10x_Visium/GSM9566413/) |
| [GSM9566414](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9566414) | Kidney_Ethanol | *Mus musculus* | kidney-alcohol-injury ([GSE323994](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE323994)) | alcohol-induced injury (Ethanol (liquid diet)) | [`GSM9566414`](sample/10x_Visium/GSM9566414/) |
| [GSM9566415](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9566415) | Kidney_Control_CCl4 | *Mus musculus* | kidney-alcohol-injury ([GSE323994](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE323994)) | CCl4 injury (Control diet + CCl4) | [`GSM9566415`](sample/10x_Visium/GSM9566415/) |
| [GSM9566416](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9566416) | Kidney_Ethanol_CCl4 | *Mus musculus* | kidney-alcohol-injury ([GSE323994](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE323994)) | alcohol and CCl4 injury (Ethanol diet + CCl4) | [`GSM9566416`](sample/10x_Visium/GSM9566416/) |
| [GSM7115963](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM7115963) | D1_kidney_AKI | *Homo sapiens* | human-cortical-AKI ([GSE228169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228169)) | acute kidney injury (acute kidney injury; day 1) | [`GSM7115963`](sample/10x_Visium/GSM7115963/) |
| [GSM7115964](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM7115964) | D15_kidney_AKI | *Homo sapiens* | human-cortical-AKI ([GSE228169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228169)) | acute kidney injury (acute kidney injury; day 15) | [`GSM7115964`](sample/10x_Visium/GSM7115964/) |
| [GSM8440997](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8440997) | Sham_No13 | *Mus musculus* | mouse-DDR1-fibrosis ([GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)) | sham control (Sham (vehicle)) | [`GSM8440997`](sample/10x_Visium/GSM8440997/) |
| [GSM8440998](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8440998) | UUO_Vehicle_No18 | *Mus musculus* | mouse-DDR1-fibrosis ([GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)) | UUO fibrosis (UUO (vehicle)) | [`GSM8440998`](sample/10x_Visium/GSM8440998/) |
| [GSM8440999](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8440999) | UUO_CH6824025_No22 | *Mus musculus* | mouse-DDR1-fibrosis ([GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)) | UUO fibrosis + DDR1 inhibitor (UUO (CH6824025)) | [`GSM8440999`](sample/10x_Visium/GSM8440999/) |
| [GSM8441000](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8441000) | UUO_CH6824025_No24 | *Mus musculus* | mouse-DDR1-fibrosis ([GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)) | UUO fibrosis + DDR1 inhibitor (UUO (CH6824025)) | [`GSM8441000`](sample/10x_Visium/GSM8441000/) |
| [GSM8441001](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8441001) | UUO_Vehicle_No16 | *Mus musculus* | mouse-DDR1-fibrosis ([GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)) | UUO fibrosis (UUO (vehicle)) | [`GSM8441001`](sample/10x_Visium/GSM8441001/) |
| [GSM8441002](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8441002) | UUO_Vehicle_No19 | *Mus musculus* | mouse-DDR1-fibrosis ([GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)) | UUO fibrosis (UUO (vehicle)) | [`GSM8441002`](sample/10x_Visium/GSM8441002/) |
| [GSM8441003](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8441003) | UUO_CH6824025_No21 | *Mus musculus* | mouse-DDR1-fibrosis ([GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)) | UUO fibrosis + DDR1 inhibitor (UUO (CH6824025)) | [`GSM8441003`](sample/10x_Visium/GSM8441003/) |
| [GSM8441004](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8441004) | UUO_CH6824025_No23 | *Mus musculus* | mouse-DDR1-fibrosis ([GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)) | UUO fibrosis + DDR1 inhibitor (UUO (CH6824025)) | [`GSM8441004`](sample/10x_Visium/GSM8441004/) |
| [GSM9034732](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9034732) | EHU_W2 | *Homo sapiens* | human-TSC-angiomyolipoma ([GSE299165](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299165)) | kidney cancer control (kidney tumor adjacent control) | [`GSM9034732`](sample/10x_Visium/GSM9034732/) |
| [GSM9034733](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9034733) | Sporadic_AML | *Homo sapiens* | human-TSC-angiomyolipoma ([GSE299165](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299165)) | sporadic angiomyolipoma (sporadic angiomyolipoma) | [`GSM9034733`](sample/10x_Visium/GSM9034733/) |
| [GSM9034734](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9034734) | TSC_AML | *Homo sapiens* | human-TSC-angiomyolipoma ([GSE299165](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299165)) | TSC-associated angiomyolipoma (tuberous sclerosis complex angiomyolipoma) | [`GSM9034734`](sample/10x_Visium/GSM9034734/) |
| [GSM9580200](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9580200) | ove26_36w | *Mus musculus* | mouse-DKD-TREM2 ([GSE324612](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324612)) | diabetic kidney disease (OVE26 diabetic kidney disease; 36 weeks) | [`GSM9580200`](sample/10x_Visium/GSM9580200/) |
| [GSM9580201](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9580201) | ove26_7w | *Mus musculus* | mouse-DKD-TREM2 ([GSE324612](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324612)) | diabetic kidney disease (OVE26 diabetic kidney disease; 7 weeks) | [`GSM9580201`](sample/10x_Visium/GSM9580201/) |
| [GSM9580202](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9580202) | ove26_19w | *Mus musculus* | mouse-DKD-TREM2 ([GSE324612](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324612)) | diabetic kidney disease (OVE26 diabetic kidney disease; 19 weeks) | [`GSM9580202`](sample/10x_Visium/GSM9580202/) |
| [GSM9580203](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9580203) | wt_control | *Mus musculus* | mouse-DKD-TREM2 ([GSE324612](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324612)) | healthy control (wild-type control) | [`GSM9580203`](sample/10x_Visium/GSM9580203/) |
| [GSM9767741](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9767741) | P1_LN | *Homo sapiens* | human-LN-spatial ([GSE333529](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE333529)) | lupus nephritis (lupus nephritis renal biopsy) | [`GSM9767741`](sample/10x_Visium/GSM9767741/) |
| [GSM9767742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9767742) | P2_LN | *Homo sapiens* | human-LN-spatial ([GSE333529](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE333529)) | lupus nephritis (lupus nephritis renal biopsy) | [`GSM9767742`](sample/10x_Visium/GSM9767742/) |
| [GSM9767743](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9767743) | P3_LN | *Homo sapiens* | human-LN-spatial ([GSE333529](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE333529)) | lupus nephritis (lupus nephritis renal biopsy) | [`GSM9767743`](sample/10x_Visium/GSM9767743/) |
| [GSM9767744](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9767744) | P4_LN | *Homo sapiens* | human-LN-spatial ([GSE333529](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE333529)) | lupus nephritis (lupus nephritis renal biopsy) | [`GSM9767744`](sample/10x_Visium/GSM9767744/) |

### 4.2 10x Genomics Visium CytAssist (14 Samples)

| GSM Accession | Sample ID | Species | Study / Series | Disease Condition / Context | Pipeline Link |
|---|---|---|---|---|---|
| [GSM8323120](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8323120) | visium_sham | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | sham (control) (bIRI sham) | [`GSM8323120`](sample/10x_Visium_CytAssist/GSM8323120/) |
| [GSM8323121](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8323121) | visium_hour4 | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8323121`](sample/10x_Visium_CytAssist/GSM8323121/) |
| [GSM8323122](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8323122) | visium_hour12 | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8323122`](sample/10x_Visium_CytAssist/GSM8323122/) |
| [GSM8323123](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8323123) | visium_day2 | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8323123`](sample/10x_Visium_CytAssist/GSM8323123/) |
| [GSM8323124](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8323124) | visium_day14 | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8323124`](sample/10x_Visium_CytAssist/GSM8323124/) |
| [GSM8323125](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8323125) | visium_week6 | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8323125`](sample/10x_Visium_CytAssist/GSM8323125/) |
| [GSM9155022](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9155022) | control_58055 | *Homo sapiens* | transplant-rejection-FCGR3A ([GSE304669](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304669)) | transplant control (kidney allograft biopsy; control) | [`GSM9155022`](sample/10x_Visium_CytAssist/GSM9155022/) |
| [GSM9155023](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9155023) | active AMR_58056 | *Homo sapiens* | transplant-rejection-FCGR3A ([GSE304669](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304669)) | transplant-AMR (kidney allograft biopsy; active AMR) | [`GSM9155023`](sample/10x_Visium_CytAssist/GSM9155023/) |
| [GSM9155024](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9155024) | acute TCMR_58057 | *Homo sapiens* | transplant-rejection-FCGR3A ([GSE304669](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304669)) | transplant-TCMR (kidney allograft biopsy; acute TCMR) | [`GSM9155024`](sample/10x_Visium_CytAssist/GSM9155024/) |
| [GSM9155025](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9155025) | chronic active AMR_58058 | *Homo sapiens* | transplant-rejection-FCGR3A ([GSE304669](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304669)) | transplant-CAMR (chronic active) (kidney allograft biopsy; chronic active AMR) | [`GSM9155025`](sample/10x_Visium_CytAssist/GSM9155025/) |
| [GSM9895920](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9895920) | ES (early stable) | *Homo sapiens* | hypertensive-nephropathy ([GSE339455](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE339455)) | hypertensive nephropathy (ES) (hypertensive nephropathy, ES) | [`GSM9895920`](sample/10x_Visium_CytAssist/GSM9895920/) |
| [GSM9895921](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9895921) | EP (early progressor) | *Homo sapiens* | hypertensive-nephropathy ([GSE339455](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE339455)) | hypertensive nephropathy (EP) (hypertensive nephropathy, EP) | [`GSM9895921`](sample/10x_Visium_CytAssist/GSM9895921/) |
| [GSM9895922](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9895922) | LS (late stable) | *Homo sapiens* | hypertensive-nephropathy ([GSE339455](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE339455)) | hypertensive nephropathy (LS) (hypertensive nephropathy, LS) | [`GSM9895922`](sample/10x_Visium_CytAssist/GSM9895922/) |
| [GSM9895923](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9895923) | LP (late progressor) | *Homo sapiens* | hypertensive-nephropathy ([GSE339455](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE339455)) | hypertensive nephropathy (LP) (hypertensive nephropathy, LP) | [`GSM9895923`](sample/10x_Visium_CytAssist/GSM9895923/) |

### 4.3 10x Genomics Visium HD (12 Samples)

| GSM Accession | Sample ID | Species | Study / Series | Disease Condition / Context | Pipeline Link |
|---|---|---|---|---|---|
| [GSM9467249](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9467249) | patient1 | *Homo sapiens* | DKD-HIF-SGLT2i ([GSE317226](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE317226)) | DKD (T2D) (type-2 diabetes, pre-SGLT2i) | [`GSM9467249`](sample/10x_Visium_HD/GSM9467249/) |
| [GSM9467250](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9467250) | patient5 | *Homo sapiens* | DKD-HIF-SGLT2i ([GSE317226](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE317226)) | DKD (T2D) (type-2 diabetes, pre-SGLT2i) | [`GSM9467250`](sample/10x_Visium_HD/GSM9467250/) |
| [GSM9467251](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9467251) | patient7 | *Homo sapiens* | DKD-HIF-SGLT2i ([GSE317226](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE317226)) | DKD (T2D) (type-2 diabetes, pre-SGLT2i) | [`GSM9467251`](sample/10x_Visium_HD/GSM9467251/) |
| [GSM9467252](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9467252) | patient9 | *Homo sapiens* | DKD-HIF-SGLT2i ([GSE317226](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE317226)) | DKD (T2D) (type-2 diabetes, pre-SGLT2i) | [`GSM9467252`](sample/10x_Visium_HD/GSM9467252/) |
| [GSM9802211](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9802211) | CAMR-ZLD_Spatial | *Homo sapiens* | CAMR-scRNA-VisiumHD ([GSE334924](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE334924)) | transplant-CAMR (chronic AMR graft biopsy) | [`GSM9802211`](sample/10x_Visium_HD/GSM9802211/) |
| [GSM9071194](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9071194) | Patient1_SSNS | *Homo sapiens* | human-nephrotic-visiumhd ([GSE300895](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300895)) | steroid-sensitive nephrotic syndrome (steroid-sensitive nephrotic syndrome (SSNS)) | [`GSM9071194`](sample/10x_Visium_HD/GSM9071194/) |
| [GSM9071195](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9071195) | Patient2_FSGS | *Homo sapiens* | human-nephrotic-visiumhd ([GSE300895](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300895)) | focal segmental glomerulosclerosis (focal segmental glomerulosclerosis (FSGS)) | [`GSM9071195`](sample/10x_Visium_HD/GSM9071195/) |
| [GSM9071196](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9071196) | Patient3_FR_SDNS | *Homo sapiens* | human-nephrotic-visiumhd ([GSE300895](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300895)) | frequently relapsing nephrotic syndrome (frequently relapsing/steroid-dependent nephrotic syndrome (FR/SDNS)) | [`GSM9071196`](sample/10x_Visium_HD/GSM9071196/) |
| [GSM10122934](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM10122934) | mouse_47822-7_ctrl | *Mus musculus* | mouse-lithium-polyuria ([GSE350835](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE350835)) | reference/normal (wild type mouse kidney control) | [`GSM10122934`](sample/10x_Visium_HD/GSM10122934/) |
| [GSM10122935](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM10122935) | mouse_47822-8_ctrl | *Mus musculus* | mouse-lithium-polyuria ([GSE350835](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE350835)) | reference/normal (wild type mouse kidney control) | [`GSM10122935`](sample/10x_Visium_HD/GSM10122935/) |
| [GSM10122936](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM10122936) | mouse_48966-1_li | *Mus musculus* | mouse-lithium-polyuria ([GSE350835](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE350835)) | lithium-induced nephropathy (lithium-induced polyuria mouse kidney) | [`GSM10122936`](sample/10x_Visium_HD/GSM10122936/) |
| [GSM10122937](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM10122937) | mouse_48966-2_li | *Mus musculus* | mouse-lithium-polyuria ([GSE350835](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE350835)) | lithium-induced nephropathy (lithium-induced polyuria mouse kidney) | [`GSM10122937`](sample/10x_Visium_HD/GSM10122937/) |

### 4.4 10x Genomics Xenium in situ (56 Samples)

| GSM Accession | Sample ID | Species | Study / Series | Disease Condition / Context | Pipeline Link |
|---|---|---|---|---|---|
| [GSM8325615](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325615) | xenium_shamL | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | sham (control) (bIRI sham) | [`GSM8325615`](sample/10x_Xenium_in_situ/GSM8325615/) |
| [GSM8325616](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325616) | xenium_shamR | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | sham (control) (bIRI sham) | [`GSM8325616`](sample/10x_Xenium_in_situ/GSM8325616/) |
| [GSM8325617](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325617) | xenium_hour4L | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8325617`](sample/10x_Xenium_in_situ/GSM8325617/) |
| [GSM8325618](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325618) | xenium_hour4R | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8325618`](sample/10x_Xenium_in_situ/GSM8325618/) |
| [GSM8325619](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325619) | xenium_hour12L | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8325619`](sample/10x_Xenium_in_situ/GSM8325619/) |
| [GSM8325620](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325620) | xenium_hour12R | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8325620`](sample/10x_Xenium_in_situ/GSM8325620/) |
| [GSM8325621](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325621) | xenium_day2L | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8325621`](sample/10x_Xenium_in_situ/GSM8325621/) |
| [GSM8325622](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325622) | xenium_day2R | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8325622`](sample/10x_Xenium_in_situ/GSM8325622/) |
| [GSM8325623](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325623) | xenium_day14L | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8325623`](sample/10x_Xenium_in_situ/GSM8325623/) |
| [GSM8325624](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325624) | xenium_day14R | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8325624`](sample/10x_Xenium_in_situ/GSM8325624/) |
| [GSM8325625](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325625) | xenium_week6L | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8325625`](sample/10x_Xenium_in_situ/GSM8325625/) |
| [GSM8325626](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325626) | xenium_week6R | *Mus musculus* | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) | AKI/IRI (bilateral IRI) (bIRI) | [`GSM8325626`](sample/10x_Xenium_in_situ/GSM8325626/) |
| [GSM8691119](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8691119) | B6→B6 syngeneic (Xenium) | *Mus musculus* | kidney-transplant-rejection ([GSE284742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284742)) | transplant (syn/allo, mouse) (syngeneic, C57BL/6→C57BL/6) | [`GSM8691119`](sample/10x_Xenium_in_situ/GSM8691119/) |
| [GSM8691120](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8691120) | BALB/c→BALB/c syn (Xenium) | *Mus musculus* | kidney-transplant-rejection ([GSE284742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284742)) | transplant (syn/allo, mouse) (syngeneic, BALB/c→BALB/c) | [`GSM8691120`](sample/10x_Xenium_in_situ/GSM8691120/) |
| [GSM8691121](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8691121) | BALB/c→B6 allo (Xenium) | *Mus musculus* | kidney-transplant-rejection ([GSE284742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284742)) | transplant (syn/allo, mouse) (allogeneic, BALB/c→C57BL/6) | [`GSM8691121`](sample/10x_Xenium_in_situ/GSM8691121/) |
| [GSM8691122](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8691122) | BALB/c→B6 allo 3 (Xenium) | *Mus musculus* | kidney-transplant-rejection ([GSE284742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284742)) | transplant (syn/allo, mouse) (allogeneic, BALB/c→C57BL/6) | [`GSM8691122`](sample/10x_Xenium_in_situ/GSM8691122/) |
| [GSM8691123](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8691123) | B6→BALB/c allo 2 (Xenium) | *Mus musculus* | kidney-transplant-rejection ([GSE284742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284742)) | transplant (syn/allo, mouse) (allogeneic, C57BL/6→BALB/c) | [`GSM8691123`](sample/10x_Xenium_in_situ/GSM8691123/) |
| [GSM8691124](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8691124) | B6→BALB/c allo (Xenium) | *Mus musculus* | kidney-transplant-rejection ([GSE284742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284742)) | transplant (syn/allo, mouse) (allogeneic, C57BL/6→BALB/c) | [`GSM8691124`](sample/10x_Xenium_in_situ/GSM8691124/) |
| [GSM8691125](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8691125) | B6→BALB/c allo 3 (Xenium) | *Mus musculus* | kidney-transplant-rejection ([GSE284742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284742)) | transplant (syn/allo, mouse) (allogeneic, C57BL/6→BALB/c) | [`GSM8691125`](sample/10x_Xenium_in_situ/GSM8691125/) |
| [GSM8717006](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8717006) | 20210907-NMK92M | *Mus musculus* | kidney-aging-xenium ([GSE286051](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286051)) | normal (aging) (normal kidney, 92 weeks, male) | [`GSM8717006`](sample/10x_Xenium_in_situ/GSM8717006/) |
| [GSM8717007](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8717007) | 20210908-NMK92F | *Mus musculus* | kidney-aging-xenium ([GSE286051](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286051)) | normal (aging) (normal kidney, 92 weeks, female) | [`GSM8717007`](sample/10x_Xenium_in_situ/GSM8717007/) |
| [GSM8717008](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8717008) | 20240208-NMK12F2 | *Mus musculus* | kidney-aging-xenium ([GSE286051](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286051)) | normal (aging) (normal kidney, 12 weeks, female) | [`GSM8717008`](sample/10x_Xenium_in_situ/GSM8717008/) |
| [GSM8717009](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8717009) | 20240208-NMK12M2 | *Mus musculus* | kidney-aging-xenium ([GSE286051](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286051)) | normal (aging) (normal kidney, 12 weeks, male) | [`GSM8717009`](sample/10x_Xenium_in_situ/GSM8717009/) |
| [GSM8720409](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720409) | kidney_xenium_1 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | reference/normal (Control human kidney biopsy) | [`GSM8720409`](sample/10x_Xenium_in_situ/GSM8720409/) |
| [GSM8720410](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720410) | kidney_xenium_2 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | reference/normal (Control human kidney biopsy) | [`GSM8720410`](sample/10x_Xenium_in_situ/GSM8720410/) |
| [GSM8720411](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720411) | kidney_xenium_3 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | diabetic kidney disease (DKD human kidney biopsy) | [`GSM8720411`](sample/10x_Xenium_in_situ/GSM8720411/) |
| [GSM8720412](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720412) | kidney_xenium_4 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | diabetic kidney disease (DKD human kidney biopsy) | [`GSM8720412`](sample/10x_Xenium_in_situ/GSM8720412/) |
| [GSM8720413](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720413) | kidney_xenium_5 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | diabetic kidney disease (DKD human kidney biopsy) | [`GSM8720413`](sample/10x_Xenium_in_situ/GSM8720413/) |
| [GSM8720414](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720414) | kidney_xenium_6 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | reference/normal (Control human kidney biopsy) | [`GSM8720414`](sample/10x_Xenium_in_situ/GSM8720414/) |
| [GSM8720415](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720415) | kidney_xenium_7 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | diabetic kidney disease (DKD human kidney biopsy) | [`GSM8720415`](sample/10x_Xenium_in_situ/GSM8720415/) |
| [GSM8720416](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720416) | kidney_xenium_8 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | diabetic kidney disease (DKD human kidney biopsy) | [`GSM8720416`](sample/10x_Xenium_in_situ/GSM8720416/) |
| [GSM8720417](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720417) | kidney_xenium_9 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | diabetic kidney disease (DKD human kidney biopsy) | [`GSM8720417`](sample/10x_Xenium_in_situ/GSM8720417/) |
| [GSM8720418](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720418) | kidney_xenium_10 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | IgA nephropathy (IgAN human kidney biopsy) | [`GSM8720418`](sample/10x_Xenium_in_situ/GSM8720418/) |
| [GSM8720419](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720419) | kidney_xenium_11 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | IgA nephropathy (IgAN human kidney biopsy) | [`GSM8720419`](sample/10x_Xenium_in_situ/GSM8720419/) |
| [GSM8720420](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720420) | kidney_xenium_12 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | IgA nephropathy (IgAN human kidney biopsy) | [`GSM8720420`](sample/10x_Xenium_in_situ/GSM8720420/) |
| [GSM8720421](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720421) | kidney_xenium_13 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | IgA nephropathy (IgAN human kidney biopsy) | [`GSM8720421`](sample/10x_Xenium_in_situ/GSM8720421/) |
| [GSM8720422](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720422) | kidney_xenium_14 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | minimal change disease (MCD human kidney biopsy) | [`GSM8720422`](sample/10x_Xenium_in_situ/GSM8720422/) |
| [GSM8720423](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720423) | kidney_xenium_15 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | minimal change disease (MCD human kidney biopsy) | [`GSM8720423`](sample/10x_Xenium_in_situ/GSM8720423/) |
| [GSM8720424](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720424) | kidney_xenium_16 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | minimal change disease (MCD human kidney biopsy) | [`GSM8720424`](sample/10x_Xenium_in_situ/GSM8720424/) |
| [GSM8720425](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720425) | kidney_xenium_17 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | minimal change disease (MCD human kidney biopsy) | [`GSM8720425`](sample/10x_Xenium_in_situ/GSM8720425/) |
| [GSM8720426](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720426) | kidney_xenium_18 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | membranous nephropathy (MN human kidney biopsy) | [`GSM8720426`](sample/10x_Xenium_in_situ/GSM8720426/) |
| [GSM8720427](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720427) | kidney_xenium_19 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | membranous nephropathy (MN human kidney biopsy) | [`GSM8720427`](sample/10x_Xenium_in_situ/GSM8720427/) |
| [GSM8720428](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720428) | kidney_xenium_20 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | membranous nephropathy (MN human kidney biopsy) | [`GSM8720428`](sample/10x_Xenium_in_situ/GSM8720428/) |
| [GSM8720429](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720429) | kidney_xenium_21 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | membranous nephropathy (MN human kidney biopsy) | [`GSM8720429`](sample/10x_Xenium_in_situ/GSM8720429/) |
| [GSM8720430](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720430) | kidney_xenium_22 | *Homo sapiens* | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) | membranous nephropathy (MN human kidney biopsy) | [`GSM8720430`](sample/10x_Xenium_in_situ/GSM8720430/) |
| [GSM9844156](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844156) | Region01 | *Homo sapiens* | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) | acute interstitial nephritis / acute tubular injury (human kidney biopsy Region01 (acute interstitial nephritis / acute tubular injury)) | [`GSM9844156`](sample/10x_Xenium_in_situ/GSM9844156/) |
| [GSM9844157](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844157) | Region02 | *Homo sapiens* | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) | acute interstitial nephritis (human kidney biopsy Region02 (acute interstitial nephritis)) | [`GSM9844157`](sample/10x_Xenium_in_situ/GSM9844157/) |
| [GSM9844158](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844158) | Region03 | *Homo sapiens* | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) | acute interstitial nephritis (human kidney biopsy Region03 (acute interstitial nephritis)) | [`GSM9844158`](sample/10x_Xenium_in_situ/GSM9844158/) |
| [GSM9844159](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844159) | Region04 | *Homo sapiens* | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) | acute tubular injury (human kidney biopsy Region04 (acute tubular injury)) | [`GSM9844159`](sample/10x_Xenium_in_situ/GSM9844159/) |
| [GSM9844160](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844160) | Region05 | *Homo sapiens* | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) | acute tubular injury (human kidney biopsy Region05 (acute tubular injury)) | [`GSM9844160`](sample/10x_Xenium_in_situ/GSM9844160/) |
| [GSM9844161](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844161) | Region09 | *Homo sapiens* | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) | acute interstitial nephritis (human kidney biopsy Region09 (acute interstitial nephritis)) | [`GSM9844161`](sample/10x_Xenium_in_situ/GSM9844161/) |
| [GSM9844162](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844162) | Region10 | *Homo sapiens* | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) | acute interstitial nephritis / acute tubular injury (human kidney biopsy Region10 (acute interstitial nephritis / acute tubular injury)) | [`GSM9844162`](sample/10x_Xenium_in_situ/GSM9844162/) |
| [GSM9844163](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844163) | Region14 | *Homo sapiens* | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) | reference/normal (human kidney biopsy Region14 (reference/normal)) | [`GSM9844163`](sample/10x_Xenium_in_situ/GSM9844163/) |
| [GSM9844164](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844164) | Region15 | *Homo sapiens* | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) | acute interstitial nephritis / acute tubular injury (human kidney biopsy Region15 (acute interstitial nephritis / acute tubular injury)) | [`GSM9844164`](sample/10x_Xenium_in_situ/GSM9844164/) |
| [GSM9792808](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9792808) | WT_Sample_A | *Mus musculus* | mouse-TAL-xenium ([GSE334656](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE334656)) | reference/normal (healthy adult mouse kidney WT_Sample_A) | [`GSM9792808`](sample/10x_Xenium_in_situ/GSM9792808/) |
| [GSM10012817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM10012817) | WT_Sample_B | *Mus musculus* | mouse-TAL-xenium ([GSE334656](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE334656)) | reference/normal (healthy adult mouse kidney WT_Sample_B) | [`GSM10012817`](sample/10x_Xenium_in_situ/GSM10012817/) |

### 4.5 NanoString CosMx SMI (3 Samples)

| GSM Accession | Sample ID | Species | Study / Series | Disease Condition / Context | Pipeline Link |
|---|---|---|---|---|---|
| [GSM8551262](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8551262) | FK1 | *Homo sapiens* | human-kidney-dev ([GSE278614](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE278614)) | fetal (healthy) (fetal, healthy) | [`GSM8551262`](sample/NanoString_CosMx_SMI/GSM8551262/) |
| [GSM8551263](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8551263) | FK4 | *Homo sapiens* | human-kidney-dev ([GSE278614](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE278614)) | fetal (healthy) (fetal, healthy) | [`GSM8551263`](sample/NanoString_CosMx_SMI/GSM8551263/) |
| [GSM8551264](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8551264) | HK3524 | *Homo sapiens* | human-kidney-dev ([GSE278614](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE278614)) | fetal (healthy) (fetal, healthy) | [`GSM8551264`](sample/NanoString_CosMx_SMI/GSM8551264/) |

### 4.6 NanoString GeoMx DSP (48 Samples)

| GSM Accession | Sample ID | Species | Study / Series | Disease Condition / Context | Pipeline Link |
|---|---|---|---|---|---|
| [GSM9938089](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938089) | ROI001 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 1; DSA+CAMR; glomerulus) | [`GSM9938089`](sample/NanoString_GeoMx_DSP/GSM9938089/) |
| [GSM9938090](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938090) | ROI002 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 1; DSA+CAMR; glomerulus) | [`GSM9938090`](sample/NanoString_GeoMx_DSP/GSM9938090/) |
| [GSM9938091](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938091) | ROI003 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 1; DSA+CAMR; glomerulus) | [`GSM9938091`](sample/NanoString_GeoMx_DSP/GSM9938091/) |
| [GSM9938092](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938092) | ROI004 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 1; DSA+CAMR; glomerulus) | [`GSM9938092`](sample/NanoString_GeoMx_DSP/GSM9938092/) |
| [GSM9938093](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938093) | ROI005 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 1; DSA+CAMR; peritubular capillary) | [`GSM9938093`](sample/NanoString_GeoMx_DSP/GSM9938093/) |
| [GSM9938094](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938094) | ROI006 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 1; DSA+CAMR; peritubular capillary) | [`GSM9938094`](sample/NanoString_GeoMx_DSP/GSM9938094/) |
| [GSM9938095](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938095) | ROI007 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 1; DSA+CAMR; peritubular capillary) | [`GSM9938095`](sample/NanoString_GeoMx_DSP/GSM9938095/) |
| [GSM9938096](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938096) | ROI008 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 1; DSA+CAMR; vessel) | [`GSM9938096`](sample/NanoString_GeoMx_DSP/GSM9938096/) |
| [GSM9938097](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938097) | ROI009 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 1; DSA+CAMR; vessel) | [`GSM9938097`](sample/NanoString_GeoMx_DSP/GSM9938097/) |
| [GSM9938098](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938098) | ROI010 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 1; DSA+CAMR; vessel) | [`GSM9938098`](sample/NanoString_GeoMx_DSP/GSM9938098/) |
| [GSM9938099](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938099) | ROI011 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 2; DSA-CAMR; glomerulus) | [`GSM9938099`](sample/NanoString_GeoMx_DSP/GSM9938099/) |
| [GSM9938100](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938100) | ROI012 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 2; DSA-CAMR; glomerulus) | [`GSM9938100`](sample/NanoString_GeoMx_DSP/GSM9938100/) |
| [GSM9938101](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938101) | ROI013 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 2; DSA-CAMR; glomerulus) | [`GSM9938101`](sample/NanoString_GeoMx_DSP/GSM9938101/) |
| [GSM9938102](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938102) | ROI014 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 2; DSA-CAMR; glomerulus) | [`GSM9938102`](sample/NanoString_GeoMx_DSP/GSM9938102/) |
| [GSM9938103](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938103) | ROI015 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 2; DSA-CAMR; peritubular capillary) | [`GSM9938103`](sample/NanoString_GeoMx_DSP/GSM9938103/) |
| [GSM9938104](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938104) | ROI016 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 2; DSA-CAMR; peritubular capillary) | [`GSM9938104`](sample/NanoString_GeoMx_DSP/GSM9938104/) |
| [GSM9938105](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938105) | ROI017 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 2; DSA-CAMR; peritubular capillary) | [`GSM9938105`](sample/NanoString_GeoMx_DSP/GSM9938105/) |
| [GSM9938106](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938106) | ROI018 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 2; DSA-CAMR; vessel) | [`GSM9938106`](sample/NanoString_GeoMx_DSP/GSM9938106/) |
| [GSM9938107](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938107) | ROI019 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 2; DSA-CAMR; vessel) | [`GSM9938107`](sample/NanoString_GeoMx_DSP/GSM9938107/) |
| [GSM9938108](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938108) | ROI020 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 2; DSA-CAMR; vessel) | [`GSM9938108`](sample/NanoString_GeoMx_DSP/GSM9938108/) |
| [GSM9938109](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938109) | ROI021 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 3; DSA+NER; glomerulus) | [`GSM9938109`](sample/NanoString_GeoMx_DSP/GSM9938109/) |
| [GSM9938110](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938110) | ROI022 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 3; DSA+NER; glomerulus) | [`GSM9938110`](sample/NanoString_GeoMx_DSP/GSM9938110/) |
| [GSM9938111](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938111) | ROI023 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 3; DSA+NER; glomerulus) | [`GSM9938111`](sample/NanoString_GeoMx_DSP/GSM9938111/) |
| [GSM9938112](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938112) | ROI024 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 3; DSA+NER; glomerulus) | [`GSM9938112`](sample/NanoString_GeoMx_DSP/GSM9938112/) |
| [GSM9938113](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938113) | ROI025 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 3; DSA+NER; peritubular capillary) | [`GSM9938113`](sample/NanoString_GeoMx_DSP/GSM9938113/) |
| [GSM9938114](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938114) | ROI026 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 3; DSA+NER; peritubular capillary) | [`GSM9938114`](sample/NanoString_GeoMx_DSP/GSM9938114/) |
| [GSM9938115](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938115) | ROI027 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 3; DSA+NER; peritubular capillary) | [`GSM9938115`](sample/NanoString_GeoMx_DSP/GSM9938115/) |
| [GSM9938116](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938116) | ROI028 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 3; DSA+NER; vessel) | [`GSM9938116`](sample/NanoString_GeoMx_DSP/GSM9938116/) |
| [GSM9938117](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938117) | ROI029 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 3; DSA+NER; vessel) | [`GSM9938117`](sample/NanoString_GeoMx_DSP/GSM9938117/) |
| [GSM9938118](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938118) | ROI030 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 3; DSA+NER; vessel) | [`GSM9938118`](sample/NanoString_GeoMx_DSP/GSM9938118/) |
| [GSM9938119](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938119) | ROI031 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 4; DSA-NER; glomerulus) | [`GSM9938119`](sample/NanoString_GeoMx_DSP/GSM9938119/) |
| [GSM9938120](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938120) | ROI032 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 4; DSA-NER; glomerulus) | [`GSM9938120`](sample/NanoString_GeoMx_DSP/GSM9938120/) |
| [GSM9938121](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938121) | ROI033 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 4; DSA-NER; glomerulus) | [`GSM9938121`](sample/NanoString_GeoMx_DSP/GSM9938121/) |
| [GSM9938122](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938122) | ROI034 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 4; DSA-NER; peritubular capillary) | [`GSM9938122`](sample/NanoString_GeoMx_DSP/GSM9938122/) |
| [GSM9938123](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938123) | ROI035 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 4; DSA-NER; peritubular capillary) | [`GSM9938123`](sample/NanoString_GeoMx_DSP/GSM9938123/) |
| [GSM9938124](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938124) | ROI036 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 4; DSA-NER; peritubular capillary) | [`GSM9938124`](sample/NanoString_GeoMx_DSP/GSM9938124/) |
| [GSM9938125](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938125) | ROI037 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 4; DSA-NER; vessel) | [`GSM9938125`](sample/NanoString_GeoMx_DSP/GSM9938125/) |
| [GSM9938126](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938126) | ROI038 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 4; DSA-NER; vessel) | [`GSM9938126`](sample/NanoString_GeoMx_DSP/GSM9938126/) |
| [GSM9938127](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938127) | ROI039 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 4; DSA-NER; vessel) | [`GSM9938127`](sample/NanoString_GeoMx_DSP/GSM9938127/) |
| [GSM9938128](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938128) | ROI040 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 5; normal control (non-transplant); glomerulus) | [`GSM9938128`](sample/NanoString_GeoMx_DSP/GSM9938128/) |
| [GSM9938129](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938129) | ROI041 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 5; normal control (non-transplant); glomerulus) | [`GSM9938129`](sample/NanoString_GeoMx_DSP/GSM9938129/) |
| [GSM9938130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938130) | ROI042 GLM | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 5; normal control (non-transplant); glomerulus) | [`GSM9938130`](sample/NanoString_GeoMx_DSP/GSM9938130/) |
| [GSM9938131](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938131) | ROI043 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 5; normal control (non-transplant); peritubular capillary) | [`GSM9938131`](sample/NanoString_GeoMx_DSP/GSM9938131/) |
| [GSM9938132](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938132) | ROI044 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 5; normal control (non-transplant); peritubular capillary) | [`GSM9938132`](sample/NanoString_GeoMx_DSP/GSM9938132/) |
| [GSM9938133](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938133) | ROI045 PTC | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 5; normal control (non-transplant); peritubular capillary) | [`GSM9938133`](sample/NanoString_GeoMx_DSP/GSM9938133/) |
| [GSM9938134](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938134) | ROI046 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 5; normal control (non-transplant); vessel) | [`GSM9938134`](sample/NanoString_GeoMx_DSP/GSM9938134/) |
| [GSM9938135](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938135) | ROI047 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 5; normal control (non-transplant); vessel) | [`GSM9938135`](sample/NanoString_GeoMx_DSP/GSM9938135/) |
| [GSM9938136](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938136) | ROI048 VSL | *Homo sapiens* | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) | transplant-CAMR (GeoMx) (kidney allograft; patient 5; normal control (non-transplant); vessel) | [`GSM9938136`](sample/NanoString_GeoMx_DSP/GSM9938136/) |

---

## 5. Platform Summary

| Platform | Samples | Typical Raw Input Format | Output AnnData Structure |
|---|---|---|---|
| **10x Visium** | 64 | Space Ranger tarball / MTX + spatial files | `obs` (spots), `obsm['spatial']`, `X` (counts) |
| **10x Visium CytAssist** | 14 | Space Ranger tarball / MTX + images | `obs` (spots), `obsm['spatial']`, `X` (counts) |
| **10x Visium HD** | 12 | 8µm bin matrices + tissue coordinates / cell segmentation | `obs` (bins/cells), `obsm['spatial']`, `X` (counts) |
| **10x Xenium in situ** | 56 | Output bundle / transcripts.zarr / flat mtx + cells.csv / cell boundaries | `obs` (cells), `obsm['spatial']`, `X` (counts) |
| **NanoString CosMx SMI** | 3 | AtoMx h5ad / raw transcripts & cell matrices | `obs` (cells), `obsm['spatial']`, `X` (counts) |
| **NanoString GeoMx DSP** | 48 | DCC count files + PKC probe annotation | `obs` (ROIs/segments), `obsm['spatial']`, `X` (counts) |

---

## 6. Disclaimer & Attribution

> [!IMPORTANT]
> **Educational & Methodological Use Only**
>
> - **Educational Purpose**: The scripts and metadata hosted in this repository are provided solely for **bioinformatics educational, methodological, and benchmarking purposes**.
> - **Consult Original Authors**: All pipelines are curated from published datasets. Users should **always consult the original publications and primary study authors** for authoritative metadata, experimental designs, and clinical context.
> - **Potential Inaccuracies**: Curation across diverse studies is subject to human error; scripts and sample descriptions in this repository may contain mislabeling, discrepancies, or inaccuracies compared to primary sources.
> - **Arbitrary QC Thresholds**: Quality control (QC) filtering parameters embedded in the scripts are baseline, arbitrary thresholds. Users must exercise their own scientific judgment to determine suitable criteria and reach their own conclusions.
> - **No Liability**: The repository maintainers assume no responsibility or liability for any errors, omissions, analytical results, or misinterpretations arising from the use of these scripts.
> - **Proper Attribution**: If you use, adapt, or reference this repository for your published studies or presentations, please cite the primary research publications and credit this repository properly.

---

## 7. License

The scripts and documentation in this repository are distributed under the [MIT License](LICENSE).
