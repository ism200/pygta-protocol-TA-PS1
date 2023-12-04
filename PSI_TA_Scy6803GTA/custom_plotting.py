# %%

import warnings
from typing import Iterable
import matplotlib.pyplot as plt
from cycler import cycler as cycler_func
from cycler import Cycler

from pyglotaran_extras.plotting.plot_concentrations import plot_concentrations
from pyglotaran_extras.plotting.plot_residual import plot_residual
from pyglotaran_extras.plotting.plot_spectra import plot_das, plot_sas
from pyglotaran_extras.plotting.plot_svd import plot_lsv_residual, plot_rsv_residual
from pyglotaran_extras.plotting.plot_traces import plot_fitted_traces
from pyglotaran_extras.plotting.style import PlotStyle

from pyglotaran_extras.types import ResultLike


def plot_concentration_and_spectra(
    result_datasets: list, cycler=None, das_cycler=None, labels=None, show_DADS=True
):
    if show_DADS:
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    else:
        fig, axes = plt.subplots(1, 2, figsize=(15, 4))
    if isinstance(cycler, list | tuple):
        cyclers = cycler
    else:
        cyclers = [cycler] * len(result_datasets)
    if labels is None:
        labels = ("A", "B", "C")
    for idx, result_dataset in enumerate(result_datasets):
        cycler = cyclers[idx]
        plot_concentrations(
            result_dataset, axes[0], center_λ=0, linlog=True, cycler=cycler
        )
        plot_sas(result_dataset, axes[1], cycler=cycler)
        if show_DADS:
            plot_das(result_dataset, axes[2], cycler=das_cycler)
    axes[0].set_xlabel("Time (ps)")
    axes[0].set_ylabel("")
    axes[0].axhline(0, color="k", linewidth=1)
    axes[1].set_xlabel("Wavelength (nm)")
    axes[1].set_ylabel("SADS (mOD)")
    axes[1].set_title("SADS")
    if show_DADS:
        axes[2].set_xlabel("Wavelength (nm)")
        axes[2].set_ylabel("DADS (mOD)")
        axes[2].set_title("DADS")
    axes[1].axhline(0, color="k", linewidth=1)
    axes[0].annotate(labels[0], xy=(-0.05, 1.02), xycoords="axes fraction", fontsize=16)
    axes[1].annotate(labels[1], xy=(-0.05, 1.02), xycoords="axes fraction", fontsize=16)
    if show_DADS:
        axes[2].annotate(
            labels[2], xy=(-0.05, 1.02), xycoords="axes fraction", fontsize=16
        )

    return fig, axes


def plot_residual_and_svd(result_datasets: list, indices=None):
    fig, axes = plt.subplots(1, 3, figsize=(10, 2))
    if indices is None:
        indices = [0]
    for result_dataset in result_datasets:
        plot_residual(result_dataset, axes[0])
        plot_lsv_residual(result_dataset, axes[1], indices=indices)
        plot_rsv_residual(result_dataset, axes[2], indices=indices)
    axes[0].get_legend().remove()
    axes[0].set_ylabel("Wavelength (nm)")
    axes[1].get_legend().remove()
    axes[1].set_ylabel("")
    axes[1].set_title("residual 1st LSV")
    axes[2].set_xlabel("Wavelength (nm)")
    axes[0].set_xlabel("Time (ps)")
    axes[1].set_xlabel("Time (ps)")
    axes[2].set_title("residual 1st RSV")
    axes[2].get_legend().remove()
    axes[2].set_ylabel("")

    return fig, axes


def _custom_cyclers_for_svd_residual():
    return (
        cycler_func(color=["k"]),
        cycler_func(color=["tab:grey"]),
        cycler_func(color=["tab:orange"]),
        cycler_func(color=["r"]),
    )


def plot_svd_of_residual(
    result_datasets: list,
    linlog,
    linthresh,
    index,
):
    fig, axes = plt.subplots(1, 2, figsize=(10, 2))
    custom_cyclers = _custom_cyclers_for_svd_residual()
    for idx, result_dataset in enumerate(result_datasets):
        custom_cycler = custom_cyclers[idx]
        plot_lsv_residual(
            result_dataset,
            axes[0],
            indices=[index],
            linlog=linlog,
            linthresh=linthresh,
            cycler=custom_cycler,
        )
        plot_rsv_residual(
            result_dataset, axes[1], indices=[index], cycler=custom_cycler
        )

    axes[0].set_xlabel("Time (ps)")
    axes[0].get_legend().remove()
    axes[0].set_ylabel("")
    axes[0].set_title("residual 1st LSV")
    axes[1].set_xlabel("Wavelength (nm)")
    axes[1].set_title("residual 1st RSV")
    axes[1].get_legend().remove()
    axes[1].set_ylabel("")
    return fig, axes


def plot_final_and_diff_EADS(result_dataset1, result_dataset2, scale=1.0):
    fig, axes = plt.subplots(1, 2, figsize=(15, 4))
    # plot_sas(global_result.data["700TR1"], axes[1], cycler=custom_cycler)
    idx1 = len(result_dataset1.species_associated_spectra.species) - 1
    idx2 = len(result_dataset2.species_associated_spectra.species) - 1
    final1 = result_dataset1.species_associated_spectra[:, idx1]
    final2 = scale * result_dataset2.species_associated_spectra[:, idx2]
    diff = final1 - final2
    final1.plot.line(x="spectral", ax=axes[0], color="k", label="700 exc")
    final2.plot.line(x="spectral", ax=axes[0], color="r", label="670 exc")
    diff.plot.line(x="spectral", ax=axes[1])
    axes[0].set_xlabel("Wavelength (nm)")
    axes[0].set_ylabel("EADS (mOD)")
    axes[0].set_title("final EADS")
    axes[0].axhline(0, color="k", linewidth=1)
    axes[1].set_xlabel("Wavelength (nm)")
    axes[1].set_ylabel("difference (mOD)")
    axes[1].set_title("difference final EADS")
    axes[1].axhline(0, color="k", linewidth=1)
    axes[0].legend()
    axes[0].annotate("A", xy=(-0.05, 1.02), xycoords="axes fraction", fontsize=16)
    axes[1].annotate("B", xy=(-0.05, 1.02), xycoords="axes fraction", fontsize=16)
    return fig, axes


def plot_fitted_traces_iscience(
    result: ResultLike,
    wavelengths: Iterable[float],
    axes_shape: tuple[int, int] = (4, 4),
    center_λ: float | None = None,
    main_irf_nr: int = 0,
    linlog: bool = False,
    linthresh: float = 1,
    divide_by_scale: bool = True,
    per_axis_legend: bool = False,
    figsize: tuple[float, float] = (30, 15),
    title: str = "Fit overview",
    y_label: str = "a.u.",
    cycler: Cycler | None = PlotStyle().data_cycler_solid,  # noqa: B008
    show_zero_line: bool = True,
):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, ax_ = plot_fitted_traces(
            result,
            wavelengths,
            linlog=linlog,
            linthresh=linthresh,
            axes_shape=axes_shape,
            figsize=figsize,
            title=title,
            per_axis_legend=per_axis_legend,
            cycler=cycler,
            # unused
            center_λ=center_λ,
            main_irf_nr=main_irf_nr,
            y_label=y_label,
            show_zero_line=show_zero_line,
            divide_by_scale=divide_by_scale,
        )
        handles, labels = ax_.flatten()[0].get_legend_handles_labels()
        for i in range(len(handles)):
            if i == 1:
                labels[i] = "670 nm excitation"
            elif i == 5:
                labels[i] = "700 nm excitation"
            else:
                labels[i] = "_Hidden"
        for idx, ax in enumerate(ax_.flatten()):
            ax.set_ylabel(ax.title.get_text().replace("spectral = ", ""))
            if idx > 1:
                ax.set_xlabel("Time (ps)")
            else:
                ax.set_xlabel("")
            ax.set_title("")
            if ax.get_legend() is not None:
                ax.get_legend().remove()
            for line in ax.lines:
                line.set_linewidth(0.5)  # Set the line width here
        fig.legend(
            handles,
            labels,
            bbox_to_anchor=(0.5, -0.05),
            loc="lower center",
            ncol=len(handles),
        )
        fig.tight_layout()
        return fig, ax_
