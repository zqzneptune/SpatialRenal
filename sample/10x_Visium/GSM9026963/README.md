# Sample GSM9026963

Processing and QC pipeline for **GSM9026963** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9026963](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9026963) |
| **Study** | kidney-PT-regen ([GSE298953](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE298953)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | reference (nephrectomy control) |
| **Condition / Timepoint** | reference kidney; nephrectomy / — |
| **Sex / Age** | M / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | fresh frozen (OCT) |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9026963](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9026963) (Series [GSE298953](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE298953)):

- `GSM9026963_V10S15-102_XY01_IU-21-019-2.tif.gz`  (180 MB, author-distributed)
- `GSM9026963_aligned_fiducials.jpg.gz`  (1 MB, author-distributed)
- `GSM9026963_detected_tissue_image.jpg.gz`  (2 MB, author-distributed)
- `GSM9026963_filtered_feature_bc_matrix.h5`  (3 MB, author-distributed)
- `GSM9026963_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9026963_tissue_hires_image.png.gz`  (3 MB, author-distributed)
- `GSM9026963_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM9026963_tissue_positions_list.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9026963_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9026963_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9026963_processed.qc.json` — Structured JSON metrics report
- `data/GSM9026963_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9026963_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM9026963

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
