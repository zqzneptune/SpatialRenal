# Sample GSM9802211

Processing and QC pipeline for **GSM9802211** (10x Visium HD).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9802211](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9802211) |
| **Study** | CAMR-scRNA-VisiumHD ([GSE334924](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE334924)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium HD |
| **Disease Condition** | transplant-CAMR |
| **Condition / Timepoint** | chronic AMR graft biopsy / — |
| **Sex / Age** | M / 40 years |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | nan |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9802211](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9802211) (Series [GSE334924](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE334924)):

- `GSM9802211_CAMR-ZLD_Spatial.tar.gz`  (329 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9802211_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9802211_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9802211_processed.qc.json` — Structured JSON metrics report
- `data/GSM9802211_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9802211_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium_HD/GSM9802211

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
