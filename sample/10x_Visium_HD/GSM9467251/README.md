# Sample GSM9467251

Processing and QC pipeline for **GSM9467251** (10x Visium HD).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9467251](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9467251) |
| **Study** | DKD-HIF-SGLT2i ([GSE317226](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE317226)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium HD |
| **Disease Condition** | DKD (T2D) |
| **Condition / Timepoint** | type-2 diabetes, pre-SGLT2i / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9467251](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9467251) (Series [GSE317226](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE317226)):

- `GSM9467251_patient7_aligned_fiducials.jpg.gz`  (3 MB, author-distributed)
- `GSM9467251_patient7_aligned_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9467251_patient7_barcodes.tsv.gz`  (1 MB, author-distributed)
- `GSM9467251_patient7_cloupe_008um.cloupe.gz`  (65 MB, author-distributed)
- `GSM9467251_patient7_cytassist_image.tiff.gz`  (22 MB, author-distributed)
- `GSM9467251_patient7_detected_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9467251_patient7_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9467251_patient7_matrix.mtx.gz`  (20 MB, author-distributed)
- `GSM9467251_patient7_microscope_image.tiff.gz`  (35 MB, author-distributed)
- `GSM9467251_patient7_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9467251_patient7_tissue_hires_image.png.gz`  (12 MB, author-distributed)
- `GSM9467251_patient7_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM9467251_patient7_tissue_positions.parquet.gz`  (11 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9467251_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9467251_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9467251_processed.qc.json` — Structured JSON metrics report
- `data/GSM9467251_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9467251_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium_HD/GSM9467251

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
