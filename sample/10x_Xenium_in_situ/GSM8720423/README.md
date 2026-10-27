# Sample GSM8720423

Processing and QC pipeline for **GSM8720423** (10x Xenium in situ).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM8720423](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720423) |
| **Study** | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Xenium in situ |
| **Disease Condition** | minimal change disease |
| **Condition / Timepoint** | MCD human kidney biopsy / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | cortex/glomerulus |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM8720423](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720423) (Series [GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)):

- `GSM8720423_kidney_xenium_15_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM8720423_kidney_xenium_15_cells.csv.gz`  (4 MB, author-distributed)
- `GSM8720423_kidney_xenium_15_features.tsv.gz`  (0 MB, author-distributed)
- `GSM8720423_kidney_xenium_15_matrix.mtx.gz`  (3 MB, author-distributed)
- `GSM8720423_kidney_xenium_15_transcripts.parquet.gz`  (40 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM8720423_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM8720423_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM8720423_processed.qc.json` — Structured JSON metrics report
- `data/GSM8720423_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM8720423_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Xenium_in_situ/GSM8720423

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
