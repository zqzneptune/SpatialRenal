# Sample GSM9895922

Processing and QC pipeline for **GSM9895922** (10x Visium CytAssist).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9895922](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9895922) |
| **Study** | hypertensive-nephropathy ([GSE339455](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE339455)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium CytAssist |
| **Disease Condition** | hypertensive nephropathy (LS) |
| **Condition / Timepoint** | hypertensive nephropathy, LS / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9895922](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9895922) (Series [GSE339455](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE339455)):

- `GSM9895922_LS_aligned_fiducials.jpg.gz`  (3 MB, author-distributed)
- `GSM9895922_LS_aligned_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9895922_LS_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM9895922_LS_cytassist_image.tiff.gz`  (21 MB, author-distributed)
- `GSM9895922_LS_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9895922_LS_matrix.mtx.gz`  (13 MB, author-distributed)
- `GSM9895922_LS_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9895922_LS_tissue_hires_image.png.gz`  (3 MB, author-distributed)
- `GSM9895922_LS_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM9895922_LS_tissue_positions.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9895922_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9895922_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9895922_processed.qc.json` — Structured JSON metrics report
- `data/GSM9895922_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9895922_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium_CytAssist/GSM9895922

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
