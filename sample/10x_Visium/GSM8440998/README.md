# Sample GSM8440998

Processing and QC pipeline for **GSM8440998** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM8440998](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8440998) |
| **Study** | mouse-DDR1-fibrosis ([GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | UUO fibrosis |
| **Condition / Timepoint** | UUO (vehicle) / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | UUO |
| **Tissue Prep** | fresh frozen (OCT) |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM8440998](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8440998) (Series [GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)):

- `GSM8440998_No18_aligned_fiducials.jpg.gz`  (1 MB, author-distributed)
- `GSM8440998_No18_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM8440998_No18_detected_tissue_image.jpg.gz`  (2 MB, author-distributed)
- `GSM8440998_No18_features.tsv.gz`  (0 MB, author-distributed)
- `GSM8440998_No18_matrix.mtx.gz`  (61 MB, author-distributed)
- `GSM8440998_No18_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM8440998_No18_tissue_hires_image.png.gz`  (3 MB, author-distributed)
- `GSM8440998_No18_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM8440998_No18_tissue_positions_list.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM8440998_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM8440998_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM8440998_processed.qc.json` — Structured JSON metrics report
- `data/GSM8440998_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM8440998_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM8440998

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
