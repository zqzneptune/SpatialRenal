# Sample GSM8551262

Processing and QC pipeline for **GSM8551262** (NanoString CosMx SMI).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM8551262](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8551262) |
| **Study** | human-kidney-dev ([GSE278614](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE278614)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / NanoString CosMx SMI |
| **Disease Condition** | fetal (healthy) |
| **Condition / Timepoint** | fetal, healthy / 18w5d |
| **Sex / Age** | nan / 18w5d |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM8551262](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8551262) (Series [GSE278614](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE278614)):

- `GSM8551262_FK1_raw.h5ad`  (792 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM8551262_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM8551262_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM8551262_processed.qc.json` — Structured JSON metrics report
- `data/GSM8551262_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM8551262_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/NanoString_CosMx_SMI/GSM8551262

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
