# Sample GSM9938108

Processing and QC pipeline for **GSM9938108** (NanoString GeoMx DSP).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9938108](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938108) |
| **Study** | CAMR-GeoMx ([GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / NanoString GeoMx DSP |
| **Disease Condition** | transplant-CAMR (GeoMx) |
| **Condition / Timepoint** | kidney allograft; patient 2; DSA-CAMR; vessel / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | vessel |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9938108](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9938108) (Series [GSE342778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342778)):

- `GSE342778_Hs_R_NGS_WTA_v1.0.pkc.gz`  (2 MB, author-distributed)
- `GSM9938108_DSP-1001660023291-D-E09.dcc.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9938108_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9938108_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9938108_processed.qc.json` — Structured JSON metrics report
- `data/GSM9938108_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9938108_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/NanoString_GeoMx_DSP/GSM9938108

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
