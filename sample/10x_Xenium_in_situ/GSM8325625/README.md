# Sample GSM8325625

Processing and QC pipeline for **GSM8325625** (10x Xenium in situ).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM8325625](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325625) |
| **Study** | mouse-IRI-repair ([GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Xenium in situ |
| **Disease Condition** | AKI/IRI (bilateral IRI) |
| **Condition / Timepoint** | bIRI / 6 wk L |
| **Sex / Age** | male / 8-10 weeks |
| **Tissue Region** | whole kidney |
| **Model Genotype** | C57BL/6J |
| **Tissue Prep** | FFPE |
| **Reference Genome** | mm10-2020-A |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM8325625](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8325625) (Series [GSE269884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269884)):

- `GSM8325625_xenium_week6L_male_baysor_segmentation.tar.gz`  (1094 MB, author-distributed)
- `GSM8325625_xenium_week6L_male_output.tar.gz`  (7280 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM8325625_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM8325625_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM8325625_processed.qc.json` — Structured JSON metrics report
- `data/GSM8325625_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM8325625_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Xenium_in_situ/GSM8325625

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
