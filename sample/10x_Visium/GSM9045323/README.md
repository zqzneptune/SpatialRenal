# Sample GSM9045323

Processing and QC pipeline for **GSM9045323** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9045323](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9045323) |
| **Study** | kidney-repair-matrix ([GSE299736](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299736)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | AKI repair |
| **Condition / Timepoint** | AKI repair; pooled WT+KO / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | WT and KO |
| **Tissue Prep** | nan |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9045323](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9045323) (Series [GSE299736](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299736)):

- `GSM9045323_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM9045323_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9045323_matrix.mtx.gz`  (77 MB, author-distributed)
- `GSM9045323_tissue_hires_image.png.gz`  (5 MB, author-distributed)
- `GSM9045323_tissue_lowres_image.png.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9045323_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9045323_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9045323_processed.qc.json` — Structured JSON metrics report
- `data/GSM9045323_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9045323_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM9045323

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
