# Sample GSM8720414

Processing and QC pipeline for **GSM8720414** (10x Xenium in situ).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM8720414](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720414) |
| **Study** | human-glomerular-xenium ([GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Xenium in situ |
| **Disease Condition** | reference/normal |
| **Condition / Timepoint** | Control human kidney biopsy / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | cortex/glomerulus |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM8720414](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8720414) (Series [GSE286184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286184)):

- `GSM8720414_kidney_xenium_6_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM8720414_kidney_xenium_6_cells.csv.gz`  (3 MB, author-distributed)
- `GSM8720414_kidney_xenium_6_features.tsv.gz`  (0 MB, author-distributed)
- `GSM8720414_kidney_xenium_6_matrix.mtx.gz`  (1 MB, author-distributed)
- `GSM8720414_kidney_xenium_6_transcripts.parquet.gz`  (5 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM8720414_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM8720414_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM8720414_processed.qc.json` — Structured JSON metrics report
- `data/GSM8720414_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM8720414_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Xenium_in_situ/GSM8720414

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
