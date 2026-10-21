"""Rebuild descriptive tables and figures from saved notebook transcriptions."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
DATASETS = ["TabularIoTAttack", "IoT-DIAD", "CICIoMT2024"]
TASKS = ["Binary", "Attack family", "Attack name"]


def main() -> None:
    frame = pd.read_csv(RESULTS / "notebook_cv_model_results.csv")
    required = {"dataset", "task", "model", "accuracy", "weighted_f1", "source_notebook"}
    if len(frame) != 93 or not required.issubset(frame.columns):
        raise ValueError("The model summary must contain 93 rows and all required columns")
    observed = set(zip(frame.dataset, frame.task))
    expected = {(d, t) for d in DATASETS for t in TASKS}
    if observed != expected:
        raise ValueError(f"Unexpected dataset/task groups: {observed ^ expected}")

    top = (
        frame.sort_values("weighted_f1", ascending=False)
        .groupby(["dataset", "task"], sort=False).head(3)
        .copy()
    )
    if len(top) != 27:
        raise ValueError("Expected 27 top-three model rows")
    top["rank"] = top.groupby(["dataset", "task"]).cumcount() + 1
    top.to_csv(RESULTS / "top_three_by_task.csv", index=False)

    colors = {"TabularIoTAttack": "#116782", "IoT-DIAD": "#b95332", "CICIoMT2024": "#557a3b"}
    markers = {"TabularIoTAttack": "o", "IoT-DIAD": "s", "CICIoMT2024": "^"}
    first = top[top["rank"] == 1]
    fig, ax = plt.subplots(figsize=(7.2, 3.7), layout="constrained")
    for index, dataset in enumerate(DATASETS):
        subset = first[first.dataset == dataset].set_index("task")
        for x, task in enumerate(TASKS):
            value = float(subset.loc[task, "weighted_f1"])
            xx = x + (index - 1) * 0.22
            ax.scatter(xx, value, s=65, marker=markers[dataset], color=colors[dataset], label=dataset if x == 0 else None)
            ax.text(xx, value + 0.008, f"{value:.3f}", ha="center", fontsize=8)
    ax.set_xticks(range(3), TASKS)
    ax.set_ylim(0.70, 1.04)
    ax.set_ylabel("Five-fold mean weighted F1")
    ax.grid(axis="y", color="#dddddd")
    ax.legend(loc="lower left", fontsize=8, frameon=False)
    fig.savefig(FIGURES / "audited_weighted_f1_by_task.png", dpi=300, facecolor="white")
    plt.close(fig)

    classes = pd.read_csv(RESULTS / "selected_class_report_metrics.csv")
    benign = classes[(classes.task == "Binary") & (classes["class"] == "benign")].set_index("dataset")
    if set(benign.index) != set(DATASETS):
        raise ValueError("Expected benign recall for each dataset")
    fig, ax = plt.subplots(figsize=(7.2, 3.8), layout="constrained")
    bars = ax.barh(DATASETS[::-1], [float(benign.loc[d, "recall_rounded"]) for d in DATASETS[::-1]],
                   color=[colors[d] for d in DATASETS[::-1]], height=0.55)
    ax.set_xlim(0, 1.02)
    ax.set_xlabel("Benign-flow recall on separate 20% split")
    ax.grid(axis="x", color="#dadfe5")
    ax.set_axisbelow(True)
    for bar in bars:
        ax.text(bar.get_width() + .012, bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():.2f}", va="center")
    fig.savefig(FIGURES / "benign_recall_by_dataset.png", dpi=300, facecolor="white")
    plt.close(fig)
    print("Validated 93 saved model summaries across 9 tasks; wrote top-three table and 2 figures")


if __name__ == "__main__":
    main()
