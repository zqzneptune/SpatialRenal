# Sample GSM10122934

Processing and QC pipeline for **GSM10122934** (10x Visium HD).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM10122934](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM10122934) |
| **Study** | mouse-lithium-polyuria ([GSE350835](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE350835)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Visium HD |
| **Disease Condition** | reference/normal |
| **Condition / Timepoint** | wild type mouse kidney control / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | wild type |
| **Tissue Prep** | FFPE |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM10122934](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM10122934) (Series [GSE350835](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE350835)):

- `GSM10122934_47822-7_H1-TTPQZZH-A1-fiducials-image-registration.json.gz`  (0 MB, author-distributed)
- `GSM10122934_47822-7_H1-TTPQZZH-A1-fiducials.json.gz`  (0 MB, author-distributed)
- `GSM10122934_47822-7_barcode_mappings.parquet.gz`  (60 MB, author-distributed)
- `GSM10122934_47822-7_cell_annotations.csv.gz`  (0 MB, author-distributed)
- `GSM10122934_47822-7_cell_filtered_feature_cell_matrix.h5`  (34 MB, author-distributed)
- `GSM10122934_47822-7_cell_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM10122934_47822-7_cell_segmentations.geojson.gz`  (11 MB, author-distributed)
- `GSM10122934_47822-7_cytassist_image.tiff.gz`  (21 MB, author-distributed)
- `GSM10122934_47822-7_instantseg_input.geojson.gz`  (159 MB, author-distributed)
- `GSM10122934_47822-7_metrics_summary.csv.gz`  (0 MB, author-distributed)
- `GSM10122934_47822-7_microscope_image.tiff.gz`  (49 MB, author-distributed)
- `GSM10122934_47822-7_nucleus_segmentations.geojson.gz`  (11 MB, author-distributed)
- `GSM10122934_47822-7_square_002um_filtered_feature_bc_matrix.h5`  (123 MB, author-distributed)
- `GSM10122934_47822-7_square_002um_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM10122934_47822-7_square_002um_tissue_positions.parquet.gz`  (167 MB, author-distributed)
- `GSM10122934_47822-7_square_008um_filtered_feature_bc_matrix.h5`  (62 MB, author-distributed)
- `GSM10122934_47822-7_square_008um_manual_annotations.csv.gz`  (0 MB, author-distributed)
- `GSM10122934_47822-7_square_008um_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM10122934_47822-7_square_008um_tissue_positions.parquet.gz`  (11 MB, author-distributed)
- `GSM10122934_47822-7_square_016um_filtered_feature_bc_matrix.h5`  (50 MB, author-distributed)
- `GSM10122934_47822-7_square_016um_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM10122934_47822-7_square_016um_tissue_positions.parquet.gz`  (3 MB, author-distributed)
- `GSM10122934_47822-7_tissue_hires_image.png.gz`  (21 MB, author-distributed)
- `GSM10122934_47822-7_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM10122934_47822-7_web_summary.html.gz`  (8 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM10122934_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM10122934_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM10122934_processed.qc.json` — Structured JSON metrics report
- `data/GSM10122934_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM10122934_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium_HD/GSM10122934

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
