# Sample GSM8717009

Processing and QC pipeline for **GSM8717009** (10x Xenium in situ).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM8717009](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8717009) |
| **Study** | kidney-aging-xenium ([GSE286051](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286051)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Xenium in situ |
| **Disease Condition** | normal (aging) |
| **Condition / Timepoint** | normal kidney, 12 weeks, male / 12 weeks |
| **Sex / Age** | male / 12 weeks |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM8717009](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8717009) (Series [GSE286051](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286051)):

- `GSM8717009_0024925_Scan1.qptiff.tiff.gz`  (467 MB, author-distributed)
- `GSM8717009_20240208-NMK12M2U1.barcodes.tsv.gz`  (1 MB, author-distributed)
- `GSM8717009_20240208-NMK12M2U1.cells.csv.gz`  (18 MB, author-distributed)
- `GSM8717009_20240208-NMK12M2U1.features.tsv.gz`  (0 MB, author-distributed)
- `GSM8717009_20240208-NMK12M2U1.matrix.mtx.gz`  (99 MB, author-distributed)
- `GSM8717009_20240208-NMK12M2U1.morphology.ome.tif.gz`  (8769 MB, author-distributed)
- `GSM8717009_20240208-NMK12M2U1.transcripts.parquet.gz`  (2066 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM8717009_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM8717009_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM8717009_processed.qc.json` — Structured JSON metrics report
- `data/GSM8717009_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM8717009_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Xenium_in_situ/GSM8717009

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
