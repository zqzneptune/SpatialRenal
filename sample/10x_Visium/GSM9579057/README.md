# Sample GSM9579057

Processing and QC pipeline for **GSM9579057** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9579057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9579057) |
| **Study** | lupus-nephritis-mouse ([GSE322686](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE322686)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | lupus nephritis |
| **Condition / Timepoint** | lupus nephritis, NZB/WF1 F1 female, 30 weeks / — |
| **Sex / Age** | female / 30 weeks |
| **Tissue Region** | whole kidney |
| **Model Genotype** | NZB/WF1 F1 |
| **Tissue Prep** | nan |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9579057](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9579057) (Series [GSE322686](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE322686)):

- `GSM9579057_s03_C1-well_aligned_fiducials.jpg.gz`  (2 MB, author-distributed)
- `GSM9579057_s03_C1-well_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM9579057_s03_C1-well_detected_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9579057_s03_C1-well_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9579057_s03_C1-well_matrix.mtx.gz`  (13 MB, author-distributed)
- `GSM9579057_s03_C1-well_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9579057_s03_C1-well_spatial_enrichment.csv.gz`  (1 MB, author-distributed)
- `GSM9579057_s03_C1-well_tissue_hires_image.png.gz`  (6 MB, author-distributed)
- `GSM9579057_s03_C1-well_tissue_lowres_image.png.gz`  (1 MB, author-distributed)
- `GSM9579057_s03_C1-well_tissue_positions.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9579057_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9579057_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9579057_processed.qc.json` — Structured JSON metrics report
- `data/GSM9579057_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9579057_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM9579057

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
