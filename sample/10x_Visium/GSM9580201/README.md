# Sample GSM9580201

Processing and QC pipeline for **GSM9580201** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9580201](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9580201) |
| **Study** | mouse-DKD-TREM2 ([GSE324612](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324612)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | diabetic kidney disease |
| **Condition / Timepoint** | OVE26 diabetic kidney disease; 7 weeks / 7 weeks |
| **Sex / Age** | nan / 7 weeks |
| **Tissue Region** | whole kidney |
| **Model Genotype** | OVE26 |
| **Tissue Prep** | fresh frozen (OCT) |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9580201](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9580201) (Series [GSE324612](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324612)):

- `GSM9580201_B1_aligned_fiducials.jpg.gz`  (1 MB, author-distributed)
- `GSM9580201_B1_detected_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9580201_B1_filtered_feature_bc_matrix.h5`  (5 MB, author-distributed)
- `GSM9580201_B1_molecule_info.h5`  (73 MB, author-distributed)
- `GSM9580201_B1_raw_feature_bc_matrix.h5`  (9 MB, author-distributed)
- `GSM9580201_B1_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9580201_B1_spatial_enrichment.csv.gz`  (1 MB, author-distributed)
- `GSM9580201_B1_tissue_hires_image.png.gz`  (5 MB, author-distributed)
- `GSM9580201_B1_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM9580201_B1_tissue_positions_list.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9580201_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9580201_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9580201_processed.qc.json` — Structured JSON metrics report
- `data/GSM9580201_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9580201_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM9580201

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
