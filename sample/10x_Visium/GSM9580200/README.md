# Sample GSM9580200

Processing and QC pipeline for **GSM9580200** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9580200](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9580200) |
| **Study** | mouse-DKD-TREM2 ([GSE324612](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324612)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | diabetic kidney disease |
| **Condition / Timepoint** | OVE26 diabetic kidney disease; 36 weeks / 36 weeks |
| **Sex / Age** | nan / 36 weeks |
| **Tissue Region** | whole kidney |
| **Model Genotype** | OVE26 |
| **Tissue Prep** | fresh frozen (OCT) |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9580200](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9580200) (Series [GSE324612](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324612)):

- `GSM9580200_A1_aligned_fiducials.jpg.gz`  (1 MB, author-distributed)
- `GSM9580200_A1_detected_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9580200_A1_filtered_feature_bc_matrix.h5`  (6 MB, author-distributed)
- `GSM9580200_A1_molecule_info.h5`  (81 MB, author-distributed)
- `GSM9580200_A1_raw_feature_bc_matrix.h5`  (9 MB, author-distributed)
- `GSM9580200_A1_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9580200_A1_spatial_enrichment.csv.gz`  (1 MB, author-distributed)
- `GSM9580200_A1_tissue_hires_image.png.gz`  (5 MB, author-distributed)
- `GSM9580200_A1_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM9580200_A1_tissue_positions_list.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9580200_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9580200_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9580200_processed.qc.json` — Structured JSON metrics report
- `data/GSM9580200_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9580200_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM9580200

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
