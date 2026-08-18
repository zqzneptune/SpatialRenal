# Sample GSM9231928

Processing and QC pipeline for **GSM9231928** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9231928](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231928) |
| **Study** | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | DKD |
| **Condition / Timepoint** | diabetic kidney disease; nephrectomy / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | nan |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9231928](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231928) (Series [GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)):

- `GSM9231928_V42N07-399_XY04_3775_aligned_fiducials.jpg.gz`  (3 MB, author-distributed)
- `GSM9231928_V42N07-399_XY04_3775_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM9231928_V42N07-399_XY04_3775_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9231928_V42N07-399_XY04_3775_matrix.mtx.gz`  (37 MB, author-distributed)
- `GSM9231928_V42N07-399_XY04_3775_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9231928_V42N07-399_XY04_3775_tissue_hires_image.png.gz`  (7 MB, author-distributed)
- `GSM9231928_V42N07-399_XY04_3775_tissue_lowres_image.png.gz`  (1 MB, author-distributed)
- `GSM9231928_V42N07-399_XY04_3775_tissue_positions.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9231928_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9231928_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9231928_processed.qc.json` — Structured JSON metrics report
- `data/GSM9231928_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9231928_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM9231928

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
