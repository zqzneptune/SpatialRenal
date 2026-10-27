# Sample GSM9566413

Processing and QC pipeline for **GSM9566413** (10x Visium).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM9566413](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9566413) |
| **Study** | kidney-alcohol-injury ([GSE323994](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE323994)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Visium |
| **Disease Condition** | control |
| **Condition / Timepoint** | Control (liquid diet) / 6 weeks |
| **Sex / Age** | nan / 18 weeks |
| **Tissue Region** | whole kidney |
| **Model Genotype** | WT (C57BL/6J) |
| **Tissue Prep** | fresh frozen (OCT) |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM9566413](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9566413) (Series [GSE323994](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE323994)):

- `GSM9566413_Control_aligned_fiducials.jpg.gz`  (2 MB, author-distributed)
- `GSM9566413_Control_barcodes.tsv.gz`  (0 MB, author-distributed)
- `GSM9566413_Control_detected_tissue_image.jpg.gz`  (1 MB, author-distributed)
- `GSM9566413_Control_features.tsv.gz`  (0 MB, author-distributed)
- `GSM9566413_Control_matrix.mtx.gz`  (25 MB, author-distributed)
- `GSM9566413_Control_scalefactors_json.json.gz`  (0 MB, author-distributed)
- `GSM9566413_Control_tissue_hires_image.png.gz`  (11 MB, author-distributed)
- `GSM9566413_Control_tissue_lowres_image.png.gz`  (1 MB, author-distributed)
- `GSM9566413_Control_tissue_positions.csv.gz`  (0 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM9566413_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM9566413_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM9566413_processed.qc.json` — Structured JSON metrics report
- `data/GSM9566413_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM9566413_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Visium/GSM9566413

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
