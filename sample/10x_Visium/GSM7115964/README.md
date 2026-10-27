# Sample GSM7115964

Processing and QC pipeline for **GSM7115964** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM7115964](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM7115964) |
| **Study** | human-cortical-AKI ([GSE228169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228169)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | acute kidney injury |
| **Condition / Timepoint** | acute kidney injury; day 15 / day 15 |
| **Sex / Age** | male / nan |
| **Tissue Region** | renal cortex |
| **Model Genotype** | nan |
| **Tissue Prep** | fresh frozen (OCT) |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM7115964](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM7115964) (Series [GSE228169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228169)):

- `GSM7115964_D15_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM7115964_D15_features.tsv.gz`  (0 MB, author-distributed)
- `GSM7115964_D15_matrix.mtx.gz`  (17 MB, author-distributed)
- `GSM7115964_D15_spatial_aligned_fiducials.jpg.gz`  (2 MB, author-distributed)
- `GSM7115964_D15_spatial_detected_tissue_image.jpg.gz`  (2 MB, author-distributed)
- `GSM7115964_D15_spatial_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM7115964_D15_spatial_tissue_hires_image.png.gz`  (14 MB, author-distributed)
- `GSM7115964_D15_spatial_tissue_lowres_image.png.gz`  (1 MB, author-distributed)
- `GSM7115964_D15_spatial_tissue_positions_list.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM7115964_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM7115964_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM7115964_processed.qc.json` — Structured JSON metrics report
- `data/GSM7115964_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM7115964_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM7115964

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
