# Sample GSM9844164

Processing and QC pipeline for **GSM9844164** (10x Xenium in situ).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9844164](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844164) |
| **Study** | human-AIN-xenium ([GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Xenium in situ |
| **Disease Condition** | acute interstitial nephritis / acute tubular injury |
| **Condition / Timepoint** | human kidney biopsy Region15 (acute interstitial nephritis / acute tubular injury) / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | cortex/medulla |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9844164](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9844164) (Series [GSE336890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE336890)):

- `GSM9844164_Region15_cell_boundaries.parquet.gz`  (10 MB, author-distributed)
- `GSM9844164_Region15_cell_feature_matrix.h5`  (27 MB, author-distributed)
- `GSM9844164_Region15_cells.parquet.gz`  (3 MB, author-distributed)
- `GSM9844164_Region15_nucleus_boundaries.parquet.gz`  (10 MB, author-distributed)
- `GSM9844164_Region15_transcripts.parquet.gz`  (463 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9844164_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9844164_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9844164_processed.qc.json` — Structured JSON metrics report
- `data/GSM9844164_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9844164_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Xenium_in_situ/GSM9844164

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
