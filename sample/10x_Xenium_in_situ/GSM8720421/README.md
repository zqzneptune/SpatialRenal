# Sample GSM8720421

Processing and QC pipeline for **GSM8720421** (10x Xenium in situ).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM8720421](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720421) |
| **Study** | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Xenium in situ |
| **Disease Condition** | IgA nephropathy |
| **Condition / Timepoint** | IgAN human kidney biopsy / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | cortex/glomerulus |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM8720421](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720421) (Series [GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)):

- `GSM8720421_kidney_xenium_13_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM8720421_kidney_xenium_13_cells.csv.gz`  (3 MB, author-distributed)
- `GSM8720421_kidney_xenium_13_features.tsv.gz`  (0 MB, author-distributed)
- `GSM8720421_kidney_xenium_13_matrix.mtx.gz`  (2 MB, author-distributed)
- `GSM8720421_kidney_xenium_13_transcripts.parquet.gz`  (13 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM8720421_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM8720421_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM8720421_processed.qc.json` — Structured JSON metrics report
- `data/GSM8720421_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM8720421_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Xenium_in_situ/GSM8720421

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
