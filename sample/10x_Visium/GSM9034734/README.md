# Sample GSM9034734

Processing and QC pipeline for **GSM9034734** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9034734](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9034734) |
| **Study** | human-TSC-angiomyolipoma ([GSE299165](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299165)) |
| **Species** | *Homo sapiens* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | TSC-associated angiomyolipoma |
| **Condition / Timepoint** | tuberous sclerosis complex angiomyolipoma / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | FFPE |
| **Reference Genome** | hg38 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9034734](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9034734) (Series [GSE299165](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299165)):

- `GSM9034734_TSC_AML_filtered_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM9034734_TSC_AML_filtered_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9034734_TSC_AML_filtered_matrix.mtx.gz`  (62 MB, author-distributed)
- `GSM9034734_TSC_AML_raw_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM9034734_TSC_AML_raw_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9034734_TSC_AML_raw_matrix.mtx.gz`  (90 MB, author-distributed)
- `GSM9034734_TSC_AML_spatial_aligned_fiducials.jpg.gz`  (2 MB, author-distributed)
- `GSM9034734_TSC_AML_spatial_aligned_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9034734_TSC_AML_spatial_cytassist_image.tiff.gz`  (21 MB, author-distributed)
- `GSM9034734_TSC_AML_spatial_detected_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9034734_TSC_AML_spatial_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9034734_TSC_AML_spatial_spatial_enrichment.csv.gz`  (1 MB, author-distributed)
- `GSM9034734_TSC_AML_spatial_tissue_hires_image.png.gz`  (4 MB, author-distributed)
- `GSM9034734_TSC_AML_spatial_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM9034734_TSC_AML_spatial_tissue_positions.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9034734_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9034734_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9034734_processed.qc.json` — Structured JSON metrics report
- `data/GSM9034734_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9034734_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM9034734

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
