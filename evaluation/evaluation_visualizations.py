"""
Evaluation plots for the RAG notebook (confusion-style matrix + charts).

Usage in Jupyter / Colab (after rag_results, ground_truth_results, and helpers exist):

    from evaluation_visualizations import plot_rag_evaluation_figures
    plot_rag_evaluation_figures(
        rag_results,
        ground_truth_results,
        queries=[q for q in sample_queries if q in ground_truth_results],
        save_prefix="eval_figs",  # optional PNG export
    )

Or paste the function body into a new notebook cell.
"""
from __future__ import annotations

import os
import re
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np

try:
    import seaborn as sns

    _HAS_SNS = True
except ImportError:
    _HAS_SNS = False

try:
    from sklearn.metrics import classification_report, confusion_matrix

    _HAS_SK = True
except ImportError:
    _HAS_SK = False


def normalize_titles(title_list: Sequence[str]) -> List[str]:
    normalized = []
    for title in title_list:
        title = title.lower()
        title = re.sub(r"[^a-z0-9 ]", "", title)
        title = title.strip()
        normalized.append(title)
    return normalized


def extract_titles_from_rag_output(text: str) -> List[str]:
    lines = text.split("\n")
    titles = []
    for line in lines:
        match = re.search(r"\d+\.\s*(.+?)\s*(\(|$)", line.strip())
        if match:
            titles.append(match.group(1))
    return titles


def compute_precision_recall_f1(
    predictions: Sequence[str], ground_truth: Sequence[str], k: int = 10
) -> Tuple[float, float, float]:
    pred_set = set(predictions[:k])
    gt_set = set(ground_truth)
    intersection = pred_set.intersection(gt_set)
    precision = len(intersection) / k if k > 0 else 0.0
    recall = len(intersection) / len(gt_set) if len(gt_set) > 0 else 0.0
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)
    return precision, recall, f1


def _build_binary_retrieval_labels(
    rag_results: Dict[str, str],
    ground_truth_results: Dict[str, Sequence[str]],
    queries: Sequence[str],
    k: int = 10,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Pool document-level labels for a 2-class confusion matrix:
      y_true=1: a ground-truth movie title (relevant)
      y_pred=1: that title appears in top-k extracted RAG titles
      y_true=0, y_pred=1: RAG predicted a title not in ground truth (false positive)
    """
    y_true: List[int] = []
    y_pred: List[int] = []
    for query in queries:
        if query not in rag_results or query not in ground_truth_results:
            continue
        rag_titles = normalize_titles(extract_titles_from_rag_output(rag_results[query]))
        gt_titles = normalize_titles(list(ground_truth_results[query]))
        pred_set = set(rag_titles[:k])
        gt_set = set(gt_titles)
        for t in gt_set:
            y_true.append(1)
            y_pred.append(1 if t in pred_set else 0)
        for t in pred_set:
            if t not in gt_set:
                y_true.append(0)
                y_pred.append(1)
    return np.asarray(y_true), np.asarray(y_pred)


def plot_rag_evaluation_figures(
    rag_results: Dict[str, str],
    ground_truth_results: Dict[str, Sequence[str]],
    queries: Sequence[str],
    k_default: int = 10,
    save_prefix: Optional[str] = None,
) -> None:
    """
    1) Confusion matrix (retrieval-style pooled over queries)
    2) Bar chart: Precision / Recall / F1 per query
    3) Line plot: avg Precision and Recall vs k=1..10
    """
    queries = [q for q in queries if q in ground_truth_results and q in rag_results]
    if not queries:
        raise ValueError("No overlapping queries between rag_results and ground_truth_results.")

    precisions, recalls, f1s, labels = [], [], [], []
    for q in queries:
        rag_titles = normalize_titles(extract_titles_from_rag_output(rag_results[q]))
        gt_titles = normalize_titles(list(ground_truth_results[q]))
        p, r, f1 = compute_precision_recall_f1(rag_titles, gt_titles, k=k_default)
        precisions.append(p)
        recalls.append(r)
        f1s.append(f1)
        labels.append(q[:50] + ("…" if len(q) > 50 else ""))

    # --- Figure 1: per-query metrics ---
    fig1, ax1 = plt.subplots(figsize=(10, max(4, 0.45 * len(queries))))
    x = np.arange(len(queries))
    w = 0.25
    ax1.bar(x - w, precisions, width=w, label="Precision@10", color="#4a90d9")
    ax1.bar(x, recalls, width=w, label="Recall@10", color="#6ea8ff")
    ax1.bar(x + w, f1s, width=w, label="F1@10", color="#2d5f9e")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=25, ha="right")
    ax1.set_ylim(0, 1.05)
    ax1.set_ylabel("Score")
    ax1.set_title("Per-query retrieval metrics (parsed top-10 titles vs Neo4j ground truth)")
    ax1.legend()
    ax1.grid(axis="y", alpha=0.3)
    fig1.tight_layout()
    if save_prefix:
        fig1.savefig(f"{save_prefix}_per_query_metrics.png", dpi=150, bbox_inches="tight")
    plt.show()

    # --- Figure 2: confusion matrix (pooled title-level) ---
    y_true, y_pred = _build_binary_retrieval_labels(
        rag_results, ground_truth_results, queries, k=k_default
    )
    if _HAS_SK and y_true.size > 0:
        cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        if _HAS_SNS:
            sns.heatmap(
                cm,
                annot=True,
                fmt="d",
                cmap="Blues",
                xticklabels=["Pred 0", "Pred 1"],
                yticklabels=["True 0", "True 1"],
                ax=ax2,
            )
            ax2.set_xlabel("Predicted (in top-10 list vs not)")
            ax2.set_ylabel("True (GT movie vs spurious prediction)")
        else:
            im = ax2.imshow(cm, cmap="Blues")
            for (i, j), v in np.ndenumerate(cm):
                ax2.text(j, i, str(v), ha="center", va="center", color="black")
            ax2.set_xticks([0, 1])
            ax2.set_yticks([0, 1])
            ax2.set_xticklabels(["Pred 0", "Pred 1"])
            ax2.set_yticklabels(["True 0", "True 1"])
            fig2.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
        ax2.set_title(
            "Confusion matrix (title-level)\n"
            "1=relevant GT title or spurious listed title; "
            "predicted 1=title appears in RAG top-k list"
        )
        fig2.tight_layout()
        if save_prefix:
            fig2.savefig(f"{save_prefix}_confusion_matrix.png", dpi=150, bbox_inches="tight")
        plt.show()

        print(classification_report(y_true, y_pred, target_names=["Neg (FP path)", "Pos (GT title)"]))
    else:
        print("Install scikit-learn for confusion matrix: pip install scikit-learn")

    # --- Figure 3: Precision / Recall vs k ---
    ks = list(range(1, 11))
    avg_p, avg_r = [], []
    for kk in ks:
        tp, tr = [], []
        for q in queries:
            rag_titles = normalize_titles(extract_titles_from_rag_output(rag_results[q]))
            gt_titles = normalize_titles(list(ground_truth_results[q]))
            p, r, _ = compute_precision_recall_f1(rag_titles, gt_titles, k=kk)
            tp.append(p)
            tr.append(r)
        avg_p.append(float(np.mean(tp)))
        avg_r.append(float(np.mean(tr)))

    fig3, ax3 = plt.subplots(figsize=(7, 4))
    ax3.plot(ks, avg_p, marker="o", label="Avg Precision@k", color="#4a90d9")
    ax3.plot(ks, avg_r, marker="s", label="Avg Recall@k", color="#2d5f9e")
    ax3.set_xticks(ks)
    ax3.set_xlabel("k (top retrieved titles from RAG answer)")
    ax3.set_ylabel("Score")
    ax3.set_ylim(0, 1.05)
    ax3.set_title("Average Precision & Recall vs k (over evaluated queries)")
    ax3.legend()
    ax3.grid(alpha=0.3)
    fig3.tight_layout()
    if save_prefix:
        fig3.savefig(f"{save_prefix}_precision_recall_vs_k.png", dpi=150, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    print("Import and call plot_rag_evaluation_figures(...) from your notebook after rag_results is populated.")
