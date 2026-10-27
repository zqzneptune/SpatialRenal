# Sample GSM10012817

Processing and QC pipeline for **GSM10012817** (10x Xenium in situ).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM10012817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM10012817) |
| **Study** | mouse-TAL-xenium ([GSE334656](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE334656)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Xenium in situ |
| **Disease Condition** | reference/normal |
| **Condition / Timepoint** | healthy adult mouse kidney WT_Sample_B / — |
| **Sex / Age** | nan / adult |
| **Tissue Region** | whole kidney (TAL) |
| **Model Genotype** | wild type |
| **Tissue Prep** | FFPE |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM10012817](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM10012817) (Series [GSE334656](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE334656)):

- `GSM10012817_Sample_B_TAL_Cell_Types.csv.gz`  (0 MB, author-distributed)
- `GSM10012817_cell_boundaries.csv.gz`  (37 MB, author-distributed)
- `GSM10012817_cell_feature_matrix.h5`  (62 MB, author-distributed)
- `GSM10012817_cells.csv.gz`  (9 MB, author-distributed)
- `GSM10012817_morphology_focus_0000.ome.tif.gz`  (375 MB, author-distributed)
- `GSM10012817_morphology_focus_0001.ome.tif.gz`  (478 MB, author-distributed)
- `GSM10012817_morphology_focus_0002.ome.tif.gz`  (407 MB, author-distributed)
- `GSM10012817_morphology_focus_0003.ome.tif.gz`  (311 MB, author-distributed)
- `GSM10012817_nucleus_boundaries.csv.gz`  (35 MB, author-distributed)
- `GSM10012817_transcripts.parquet.gz`  (1881 MB, author-distributed)
- `GSM10012817_xso_083026_sample_b.rds`  (4670 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM10012817_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM10012817_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM10012817_processed.qc.json` — Structured JSON metrics report
- `data/GSM10012817_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM10012817_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Xenium_in_situ/GSM10012817

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
