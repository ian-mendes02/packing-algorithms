import matplotlib.pyplot as plt
import numpy as np

from .objects import BenchmarkMetrics
from src.config import benchmark as config

_source_metrics: list[BenchmarkMetrics]
_input_sizes: np.ndarray
_gga_color = config.colors.get("gga") or "#ff7f0e"
_ffd_color = config.colors.get("ffd") or "#1f77b4"

plt.style.use(
    (
        "seaborn-v0_8-whitegrid"
        if "seaborn-v0_8-whitegrid" in plt.style.available
        else "default"
    ),
)


def source(metrics: list[BenchmarkMetrics]) -> None:
    global _input_sizes, _source_metrics
    _source_metrics = metrics
    _input_sizes = np.array([m.input_size for m in metrics])


def plot_occupation_ratio_graph() -> None:
    avg_gga_ratios = np.array(
        [
            np.mean([r.avg_occupation_ratio * 100 for r in m.gga_results])
            for m in _source_metrics
        ],
    )

    avg_ffd_ratios = np.array(
        [
            np.mean([r.avg_occupation_ratio * 100 for r in m.ffd_results])
            for m in _source_metrics
        ],
    )

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

    ax.plot(
        _input_sizes,
        avg_ffd_ratios,
        marker="o",
        linewidth=2,
        markersize=8,
        label="FFD-3D",
        color=_ffd_color,
        linestyle="--",
    )

    ax.plot(
        _input_sizes,
        avg_gga_ratios,
        marker="s",
        linewidth=2,
        markersize=8,
        label="GGA",
        color=_gga_color,
    )

    ax.set_ylabel(
        config.export["occupation_ratio"].ylabel,
        fontsize=11,
    )
    ax.set_xlabel(
        config.export["occupation_ratio"].xlabel,
        fontsize=11,
    )
    ax.set_title(
        label=config.export["occupation_ratio"].title,
        fontsize=12,
        fontweight="bold",
        pad=15,
    )
    ax.set_ybound(lower=0, upper=100)
    ax.grid(True, linestyle=":", alpha=0.7)
    ax.legend(loc="lower right", frameon=True, facecolor="white")

    plt.tight_layout()
    plt.savefig(
        config.export["occupation_ratio"].path,
        dpi=300,
        bbox_inches="tight",
    )


def plot_execution_times_graph():
    ffd_execution_times = np.array(
        [
            np.mean([r.execution_time for r in m.ffd_results])
            for m in _source_metrics
        ],
    )

    gga_execution_times = np.array(
        [
            np.mean([r.execution_time for r in m.gga_results])
            for m in _source_metrics
        ],
    )

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

    x = np.arange(len(_input_sizes))
    width = 0.35

    ffd_bars = ax.bar(
        x - width / 2,
        ffd_execution_times,
        width,
        label="FFD-3D",
        color=_ffd_color,
    )
    gga_bars = ax.bar(
        x + width / 2,
        gga_execution_times,
        width,
        label="GGA",
        color=_gga_color,
    )

    ax.set_ylabel(
        config.export["execution_times"].ylabel,
        fontsize=11,
    )
    ax.set_xlabel(
        config.export["execution_times"].xlabel,
        fontsize=11,
    )
    ax.set_title(
        label=config.export["execution_times"].title,
        fontsize=12,
        fontweight="bold",
        pad=15,
    )
    ax.set_xticks(x, labels=_input_sizes, fontsize=8)
    ax.legend(frameon=True, facecolor="white", edgecolor="none")

    ax.set_yscale("log")

    ax.bar_label(ffd_bars, padding=3, fmt="%.1f", fontsize=8)
    ax.bar_label(gga_bars, padding=3, fmt="%.0f", fontsize=8)

    plt.tight_layout()

    plt.savefig(
        config.export["execution_times"].path,
        dpi=300,
        bbox_inches="tight",
    )


def plot_parcel_count_graph():
    ffd_parcel_count = np.array(
        [
            np.mean([r.num_parcels for r in m.ffd_results])
            for m in _source_metrics
        ],
    )

    gga_parcel_count = np.array(
        [
            np.mean([r.num_parcels for r in m.gga_results])
            for m in _source_metrics
        ],
    )

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

    ax.plot(
        _input_sizes,
        ffd_parcel_count,
        marker="o",
        linewidth=2,
        markersize=8,
        label="FFD-3D",
        color=_ffd_color,
        linestyle="--",
    )

    ax.plot(
        _input_sizes,
        gga_parcel_count,
        marker="s",
        linewidth=2,
        markersize=8,
        label="GGA",
        color=_gga_color,
    )

    ax.set_ylabel(
        config.export["parcel_count"].ylabel,
        fontsize=11,
    )
    ax.set_xlabel(
        config.export["parcel_count"].xlabel,
        fontsize=11,
    )
    ax.set_title(
        config.export["parcel_count"].title,
        fontsize=12,
        fontweight="bold",
        pad=15,
    )
    ax.grid(True, linestyle=":", alpha=0.7)
    ax.set_ybound(lower=0)
    ax.legend(loc="lower right", frameon=True, facecolor="white")

    plt.tight_layout()
    plt.savefig(
        config.export["parcel_count"].path,
        dpi=300,
        bbox_inches="tight",
    )
