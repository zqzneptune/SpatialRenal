# Sample GSM9844159

Processing and QC pipeline for **GSM9844159** (10x Xenium in situ).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9844159](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844159) |
| **Study** | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Xenium in situ |
| **Disease Condition** | acute tubular injury |
| **Condition / Timepoint** | human kidney biopsy Region04 (acute tubular injury) / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | cortex |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9844159](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844159) (Series [GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)):

- `GSM9844159_Region04_cell_boundaries.parquet.gz`  (1 MB, author-distributed)
- `GSM9844159_Region04_cell_feature_matrix.h5`  (4 MB, author-distributed)
- `GSM9844159_Region04_cells.parquet.gz`  (0 MB, author-distributed)
- `GSM9844159_Region04_morphology.ome.tif.gz`  (798 MB, author-distributed)
- `GSM9844159_Region04_nucleus_boundaries.parquet.gz`  (1 MB, author-distributed)
- `GSM9844159_Region04_transcripts.parquet.gz`  (61 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9844159_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9844159_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9844159_processed.qc.json` — Structured JSON metrics report
- `data/GSM9844159_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9844159_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Xenium_in_situ/GSM9844159

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
