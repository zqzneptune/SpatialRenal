# Sample GSM8691121

Processing and QC pipeline for **GSM8691121** (10x Xenium in situ).

## Sample Metadata

| Field | Value |
|---|---|
| **GSM** | [GSM8691121](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8691121) |
| **Study** | kidney-transplant-rejection ([GSE284742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284742)) |
| **Species** | *Mus musculus* |
| **Modality / Platform** | spatial / 10x Xenium in situ |
| **Disease Condition** | transplant (syn/allo, mouse) |
| **Condition / Timepoint** | allogeneic, BALB/c→C57BL/6 / — |
| **Sex / Age** | nan / nan |
| **Tissue Region** | whole kidney (transplant) |
| **Model Genotype** | C57BL/6 / BALB/c donor→recipient |
| **Tissue Prep** | FFPE |
| **Reference Genome** | mm10 |

## Raw Data Files

To process this sample, obtain the raw author-distributed file(s) from GEO accession [GSM8691121](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM8691121) (Series [GSE284742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284742)):

- `GSM8691121_bc.bl6.1.morphology.ome.tif.gz`  (4438 MB, author-distributed)
- `GSM8691121_bc.bl6.1.transcripts.zarr.zip`  (1677 MB, author-distributed)

## Generated Outputs

Executing `process.py` produces the following standardized artifacts:

- `raw/GSM8691121_raw_counts.h5` — **Pre-QC** raw count matrix (h5ad-compatible HDF5; un-filtered, coordinates included)
- `data/GSM8691121_processed.h5` — **QC-filtered** AnnData object (h5ad-compatible HDF5; `X` = counts, `obs` = metadata & QC annotations, `obsm['spatial']` = spatial coordinates)
- `data/GSM8691121_processed.qc.json` — Structured JSON metrics report
- `data/GSM8691121_qc_report.txt` — Human-readable QC log and threshold summary
- `data/GSM8691121_umi_counts.png` — Spatial UMI count overlay plot on tissue/fluorescence image

## Running the Processing Pipeline

```bash
# 1. Ensure required Python environment is active (see repository root README.md)

# 2. Navigate to this sample directory
cd sample/10x_Xenium_in_situ/GSM8691121

# 3. Create required directory structure and place raw file(s) in raw/
mkdir -p raw data tmp

# 4. Run the ingestion & QC pipeline
python process.py --raw-dir raw --data-dir data --tmp-dir tmp
```
