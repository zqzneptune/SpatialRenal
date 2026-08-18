# Sample GSM9155023

Processing and QC pipeline for **GSM9155023** (10x Visium CytAssist).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9155023](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9155023) |
| **Study** | transplant-rejection-FCGR3A ([GSE304669](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304669)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium CytAssist |
| **Disease Condition** | transplant-AMR |
| **Condition / Timepoint** | kidney allograft biopsy; active AMR / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | nan |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9155023](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9155023) (Series [GSE304669](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304669)):

- `GSM9155023_active_AMR_58056_aligned_fiducials.jpg.gz`  (3 MB, author-distributed)
- `GSM9155023_active_AMR_58056_aligned_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9155023_active_AMR_58056_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM9155023_active_AMR_58056_cytassist_image.tiff.gz`  (21 MB, author-distributed)
- `GSM9155023_active_AMR_58056_detected_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9155023_active_AMR_58056_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9155023_active_AMR_58056_matrix.mtx.gz`  (11 MB, author-distributed)
- `GSM9155023_active_AMR_58056_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9155023_active_AMR_58056_spatial_enrichment.csv.gz`  (1 MB, author-distributed)
- `GSM9155023_active_AMR_58056_tissue_hires_image.png.gz`  (3 MB, author-distributed)
- `GSM9155023_active_AMR_58056_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM9155023_active_AMR_58056_tissue_positions.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9155023_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9155023_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9155023_processed.qc.json` — Structured JSON metrics report
- `data/GSM9155023_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9155023_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium_CytAssist/GSM9155023

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
