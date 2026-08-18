# Sample GSM9231919

Processing and QC pipeline for **GSM9231919** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9231919](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231919) |
| **Study** | DKD-MEF2C ([GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | DKD |
| **Condition / Timepoint** | diabetic kidney disease; biopsy / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | nan |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9231919](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9231919) (Series [GSE307817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307817)):

- `GSM9231919_V42N07-395_XY04_IU94_aligned_fiducials.jpg.gz`  (3 MB, author-distributed)
- `GSM9231919_V42N07-395_XY04_IU94_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM9231919_V42N07-395_XY04_IU94_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9231919_V42N07-395_XY04_IU94_matrix.mtx.gz`  (13 MB, author-distributed)
- `GSM9231919_V42N07-395_XY04_IU94_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9231919_V42N07-395_XY04_IU94_tissue_hires_image.png.gz`  (1 MB, author-distributed)
- `GSM9231919_V42N07-395_XY04_IU94_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM9231919_V42N07-395_XY04_IU94_tissue_positions.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9231919_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9231919_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9231919_processed.qc.json` — Structured JSON metrics report
- `data/GSM9231919_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9231919_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM9231919

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
