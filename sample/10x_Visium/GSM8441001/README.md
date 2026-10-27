# Sample GSM8441001

Processing and QC pipeline for **GSM8441001** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM8441001](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8441001) |
| **Study** | mouse-DDR1-fibrosis ([GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | UUO fibrosis |
| **Condition / Timepoint** | UUO (vehicle) / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | UUO |
| **Tissue Prep** | fresh frozen (OCT) |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM8441001](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8441001) (Series [GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)):

- `GSM8441001_No16_aligned_fiducials.jpg.gz`  (1 MB, author-distributed)
- `GSM8441001_No16_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM8441001_No16_detected_tissue_image.jpg.gz`  (2 MB, author-distributed)
- `GSM8441001_No16_features.tsv.gz`  (0 MB, author-distributed)
- `GSM8441001_No16_matrix.mtx.gz`  (62 MB, author-distributed)
- `GSM8441001_No16_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM8441001_No16_tissue_hires_image.png.gz`  (3 MB, author-distributed)
- `GSM8441001_No16_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM8441001_No16_tissue_positions_list.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM8441001_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM8441001_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM8441001_processed.qc.json` — Structured JSON metrics report
- `data/GSM8441001_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM8441001_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM8441001

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
