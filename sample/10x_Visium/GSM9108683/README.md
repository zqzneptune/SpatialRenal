# Sample GSM9108683

Processing and QC pipeline for **GSM9108683** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9108683](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9108683) |
| **Study** | ANCA-vasculitis ([GSE302677](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE302677)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | control |
| **Condition / Timepoint** | kidney cortex, control / — |
| **Sex / Age** | nan / pediatric |
| **Tissue Region** | kidney cortex |
| **Model Genotype** | nan |
| **Tissue Prep** | nan |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9108683](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9108683) (Series [GSE302677](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE302677)):

- `GSM9108683_ctrl_aligned_fiducials.jpg.gz`  (1 MB, author-distributed)
- `GSM9108683_ctrl_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM9108683_ctrl_detected_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9108683_ctrl_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9108683_ctrl_matrix.mtx.gz`  (8 MB, author-distributed)
- `GSM9108683_ctrl_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9108683_ctrl_tissue_hires_image.png.gz`  (4 MB, author-distributed)
- `GSM9108683_ctrl_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM9108683_ctrl_tissue_positions.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9108683_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9108683_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9108683_processed.qc.json` — Structured JSON metrics report
- `data/GSM9108683_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9108683_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM9108683

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
