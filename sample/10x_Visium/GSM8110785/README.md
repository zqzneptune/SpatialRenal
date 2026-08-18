# Sample GSM8110785

Processing and QC pipeline for **GSM8110785** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM8110785](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8110785) |
| **Study** | hyperuricemia-mouse ([GSE258959](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE258959)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | hyperuricemia (Uox-KO) |
| **Condition / Timepoint** | Uox-KO (hyperuricemia), male, C57BL/6J / — |
| **Sex / Age** | male / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | C57BL/6J; Uox-KO |
| **Tissue Prep** | nan |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM8110785](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8110785) (Series [GSE258959](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE258959)):

- `GSM8110785_Sample_JZ23087189-23209_UoxKO4-23209_UoxKO4-barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM8110785_Sample_JZ23087189-23209_UoxKO4-23209_UoxKO4-features.tsv.gz`  (0 MB, author-distributed)
- `GSM8110785_Sample_JZ23087189-23209_UoxKO4-23209_UoxKO4-matrix.mtx.gz`  (43 MB, author-distributed)
- `GSM8110785_Sample_JZ23087189-23209_UoxKO4-23209_UoxKO4-spatial.tar.gz`  (12 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM8110785_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM8110785_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM8110785_processed.qc.json` — Structured JSON metrics report
- `data/GSM8110785_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM8110785_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM8110785

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
