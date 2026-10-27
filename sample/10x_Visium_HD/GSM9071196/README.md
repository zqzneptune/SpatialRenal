# Sample GSM9071196

Processing and QC pipeline for **GSM9071196** (10x Visium HD).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9071196](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9071196) |
| **Study** | human-nephrotic-visiumhd ([GSE300895](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300895)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium HD |
| **Disease Condition** | frequently relapsing nephrotic syndrome |
| **Condition / Timepoint** | frequently relapsing/steroid-dependent nephrotic syndrome (FR/SDNS) / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9071196](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9071196) (Series [GSE300895](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300895)):

- `GSM9071196_7_A1_aligned_fiducials.jpg.gz`  (3 MB, author-distributed)
- `GSM9071196_7_A1_aligned_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9071196_7_A1_barcodes.tsv.gz`  (11 MB, author-distributed)
- `GSM9071196_7_A1_cytassist_image.tiff.gz`  (23 MB, author-distributed)
- `GSM9071196_7_A1_detected_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9071196_7_A1_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9071196_7_A1_matrix.mtx.gz`  (15 MB, author-distributed)
- `GSM9071196_7_A1_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9071196_7_A1_tissue_hires_image.png.gz`  (29 MB, author-distributed)
- `GSM9071196_7_A1_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM9071196_7_A1_tissue_positions.parquet.gz`  (169 MB, author-distributed)
- `GSM9071196_Image7.tif.gz`  (141 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9071196_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9071196_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9071196_processed.qc.json` — Structured JSON metrics report
- `data/GSM9071196_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9071196_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium_HD/GSM9071196

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
