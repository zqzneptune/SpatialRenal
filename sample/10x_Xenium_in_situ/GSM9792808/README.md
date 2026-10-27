# Sample GSM9792808

Processing and QC pipeline for **GSM9792808** (10x Xenium in situ).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9792808](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9792808) |
| **Study** | mouse-TAL-xenium ([GSE334656](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE334656)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Xenium in situ |
| **Disease Condition** | reference/normal |
| **Condition / Timepoint** | healthy adult mouse kidney WT_Sample_A / — |
| **Sex / Age** | nan / adult |
| **Tissue Region** | whole kidney (TAL) |
| **Model Genotype** | wild type |
| **Tissue Prep** | FFPE |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9792808](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9792808) (Series [GSE334656](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE334656)):

- `GSM9792808_Sample_A_TAL_Cell_Types.csv.gz`  (0 MB, author-distributed)
- `GSM9792808_cell_boundaries.csv.gz`  (39 MB, author-distributed)
- `GSM9792808_cell_feature_matrix.h5`  (77 MB, author-distributed)
- `GSM9792808_cells.csv.gz`  (10 MB, author-distributed)
- `GSM9792808_morphology_focus_0000.ome.tif.gz`  (420 MB, author-distributed)
- `GSM9792808_morphology_focus_0001.ome.tif.gz`  (587 MB, author-distributed)
- `GSM9792808_morphology_focus_0002.ome.tif.gz`  (489 MB, author-distributed)
- `GSM9792808_morphology_focus_0003.ome.tif.gz`  (361 MB, author-distributed)
- `GSM9792808_nucleus_boundaries.csv.gz`  (36 MB, author-distributed)
- `GSM9792808_transcripts.parquet.gz`  (2315 MB, author-distributed)
- `GSM9792808_xso_sample_a.rds`  (5090 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9792808_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9792808_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9792808_processed.qc.json` — Structured JSON metrics report
- `data/GSM9792808_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9792808_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Xenium_in_situ/GSM9792808

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
