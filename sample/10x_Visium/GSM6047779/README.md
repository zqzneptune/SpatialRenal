# Sample GSM6047779

Processing and QC pipeline for **GSM6047779** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM6047779](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM6047779) |
| **Study** | kidney-PT-regen ([GSE298953](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE298953)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | reference (nephrectomy control) |
| **Condition / Timepoint** | reference kidney; reused from GSE183456 / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | nan |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM6047779](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM6047779) (Series [GSE298953](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE298953)):

- `GSE298953_GSM6047779_V10S15-102_XY02_IU-21-019-5.tar.gz`  (11 MB, author-distributed)
- `GSE298953_GSM6047779_V10S15-102_XY02_IU-21-019-5.tif.gz`  (180 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM6047779_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM6047779_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM6047779_processed.qc.json` — Structured JSON metrics report
- `data/GSM6047779_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM6047779_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM6047779

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
