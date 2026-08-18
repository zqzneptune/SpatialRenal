# Sample GSM9247138

Processing and QC pipeline for **GSM9247138** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9247138](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247138) |
| **Study** | EPO-cell-neighborhood ([GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | EPO/hypoxia model |
| **Condition / Timepoint** | UUO 3d, ligated / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | nan |
| **Tissue Prep** | nan |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9247138](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9247138) (Series [GSE308511](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308511)):

- `GSM9247138_Exp36_3d_SK1440_LIG_aligned_fiducials.jpg.gz`  (2 MB, author-distributed)
- `GSM9247138_Exp36_3d_SK1440_LIG_aligned_tissue_image.jpg.gz`  (2 MB, author-distributed)
- `GSM9247138_Exp36_3d_SK1440_LIG_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM9247138_Exp36_3d_SK1440_LIG_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9247138_Exp36_3d_SK1440_LIG_matrix.mtx.gz`  (47 MB, author-distributed)
- `GSM9247138_Exp36_3d_SK1440_LIG_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9247138_Exp36_3d_SK1440_LIG_tissue_hires_image.png.gz`  (6 MB, author-distributed)
- `GSM9247138_Exp36_3d_SK1440_LIG_tissue_lowres_image.png.gz`  (1 MB, author-distributed)
- `GSM9247138_Exp36_3d_SK1440_LIG_tissue_positions.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9247138_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9247138_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9247138_processed.qc.json` — Structured JSON metrics report
- `data/GSM9247138_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9247138_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM9247138

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
