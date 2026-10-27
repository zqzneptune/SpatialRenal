# Sample GSM8441000

Processing and QC pipeline for **GSM8441000** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM8441000](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8441000) |
| **Study** | mouse-DDR1-fibrosis ([GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | UUO fibrosis + DDR1 inhibitor |
| **Condition / Timepoint** | UUO (CH6824025) / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney |
| **Model Genotype** | UUO |
| **Tissue Prep** | fresh frozen (OCT) |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM8441000](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8441000) (Series [GSE273978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273978)):

- `GSM8441000_No24_aligned_fiducials.jpg.gz`  (1 MB, author-distributed)
- `GSM8441000_No24_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM8441000_No24_detected_tissue_image.jpg.gz`  (2 MB, author-distributed)
- `GSM8441000_No24_features.tsv.gz`  (0 MB, author-distributed)
- `GSM8441000_No24_matrix.mtx.gz`  (79 MB, author-distributed)
- `GSM8441000_No24_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM8441000_No24_tissue_hires_image.png.gz`  (3 MB, author-distributed)
- `GSM8441000_No24_tissue_lowres_image.png.gz`  (0 MB, author-distributed)
- `GSM8441000_No24_tissue_positions_list.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM8441000_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM8441000_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM8441000_processed.qc.json` — Structured JSON metrics report
- `data/GSM8441000_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM8441000_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM8441000

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
