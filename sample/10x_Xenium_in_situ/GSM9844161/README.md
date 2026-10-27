# Sample GSM9844161

Processing and QC pipeline for **GSM9844161** (10x Xenium in situ).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9844161](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844161) |
| **Study** | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Xenium in situ |
| **Disease Condition** | acute interstitial nephritis |
| **Condition / Timepoint** | human kidney biopsy Region09 (acute interstitial nephritis) / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | cortex |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9844161](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844161) (Series [GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)):

- `GSM9844161_Region09_cell_boundaries.parquet.gz`  (2 MB, author-distributed)
- `GSM9844161_Region09_cell_feature_matrix.h5`  (2 MB, author-distributed)
- `GSM9844161_Region09_cells.parquet.gz`  (0 MB, author-distributed)
- `GSM9844161_Region09_morphology.ome.tif.gz`  (734 MB, author-distributed)
- `GSM9844161_Region09_nucleus_boundaries.parquet.gz`  (2 MB, author-distributed)
- `GSM9844161_Region09_transcripts.parquet.gz`  (23 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9844161_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9844161_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9844161_processed.qc.json` — Structured JSON metrics report
- `data/GSM9844161_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9844161_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Xenium_in_situ/GSM9844161

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
