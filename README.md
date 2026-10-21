# IoT and IoMT intrusion-detection benchmark audit

Companion code and saved evidence for **Binary and Attack-Level Intrusion Detection in IoT and IoMT: An Audit of Three Benchmark Evaluations**. The paper audits three analyzed CSV files and nine machine-learning notebooks. This repository contains the nine original notebooks with their saved outputs, a transcription of 93 printed model--task summaries, two paper figures, and scripts for rebuilding the summary table and figures from those saved summaries. It does **not** contain the source datasets or claim to reproduce model training in a clean environment.

## Repository contents

- `notebooks/`: nine original ML notebooks, organized by resource and target. Outputs and execution order are preserved. See `results/notebook_manifest.csv` for their original archive paths and SHA-256 hashes.
- `results/notebook_cv_model_results.csv`: 93 model--task records transcribed from the notebooks' printed five-fold mean tables. This file is a transcription, not independent fold-level output.
- `results/selected_class_report_metrics.csv`: the six rounded class-level recall values cited in the paper, from separate stratified 20% split reports.
- `results/dataset_manifest.csv`: SHA-256 fingerprints, dimensions, and provider pages for the three analyzed CSVs. No dataset file is included.
- `figures/`: the two figures used in the paper.
- `scripts/rebuild_summary.py`: validates the saved result table and regenerates a top-three table and both figures from the included CSVs.

## Rebuild the paper summaries

From the repository root:

```bash
python -m pip install -r requirements-analysis.txt
python scripts/rebuild_summary.py
```

The command checks the nine dataset--target groups, writes `results/top_three_by_task.csv`, and redraws the figures. It does **not** refit any classifier or recreate an independent evaluation. The script needs no original dataset files. The provided PNGs are the images used in the manuscript; regenerated images may have minor layout differences.

## Obtain data for notebook exploration

The provider pages are:

1. [CIC-BCCC-NRC TabularIoTAttack-2024](https://www.unb.ca/cic/datasets/tabular-iot-attack-2024.html)
2. [CIC IoT-DIAD 2024](https://www.unb.ca/cic/datasets/iot-diad-2024.html)
3. [CICIoMT2024](https://www.unb.ca/cic/datasets/iomt-dataset-2024.html), using the Wi-Fi/MQTT subset

The notebooks read **preassembled** CSVs with the filenames in `results/dataset_manifest.csv`, not necessarily the provider's raw downloads. The source preparation history and original Python package versions are incomplete, so downloading the provider datasets alone is not guaranteed to recreate the exact analyzed files or printed scores. If you possess the matching analyzed files, compare their SHA-256 hashes with the manifest before using them. The original notebooks expect the relevant CSV beside the notebook; the medical-device notebooks expect it at `WiFI_and_MQTT/balanced_dataset.csv` relative to their working directory. A full training rerun may also require `numpy`, `scikit-learn`, `imbalanced-learn`, `xgboost`, `lightgbm`, `catboost`, `torch`, `tqdm`, `seaborn`, and `jupyter`. Their original versions were not captured, so no false lockfile is provided.

## Interpretation limits

The nine notebook comparisons use random stratified five-fold splits within each resource. Full-data outlier clipping precedes splitting, and no device-grouped, time-based, or external-dataset evaluation is available. Eight of nine notebooks have non-monotonic cell execution counts. The 20% split reports are separate descriptive checks, not external holdouts; their rounded recall values are not fold averages. The audit therefore supports verification of **reported saved outputs**, not a claim of leakage-free or clinical generalization. The compilation dataset includes a CICIoMT-derived source, so these resources must not be assumed independent without a record-level provenance audit.

No reuse license is supplied here because the authors have not selected one. The original dataset providers retain their own terms and citation requirements.
