# %%
import matplotlib.pyplot as plt
from cycler import cycler
from pyglotaran_extras.plotting.plot_concentrations import plot_concentrations
from pyglotaran_extras.plotting.plot_residual import plot_residual
from pyglotaran_extras.plotting.plot_spectra import plot_das, plot_sas
from pyglotaran_extras.plotting.plot_svd import plot_lsv_residual, plot_rsv_residual


def plot_concentration_and_spectra(result_datasets: list, cycler=None, das_cycler=None):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for result_dataset in result_datasets:
        plot_concentrations(
            result_dataset, axes[0], center_λ=0, linlog=True, cycler=cycler
        )
        plot_sas(result_dataset, axes[1], cycler=cycler)
        plot_das(result_dataset, axes[2], cycler=das_cycler)
    axes[0].set_xlabel("Time (ps)")
    axes[0].set_ylabel("")
    axes[0].axhline(0, color="k", linewidth=1)
    axes[1].set_xlabel("Wavelength (nm)")
    axes[1].set_ylabel("SADS (mOD)")
    axes[1].set_title("SADS")
    axes[2].set_xlabel("Wavelength (nm)")
    axes[2].set_ylabel("DADS (mOD)")
    axes[2].set_title("DADS")
    axes[1].axhline(0, color="k", linewidth=1)
    axes[0].annotate("A", xy=(-0.05, 1.02), xycoords="axes fraction", fontsize=16)
    axes[1].annotate("B", xy=(-0.05, 1.02), xycoords="axes fraction", fontsize=16)
    axes[2].annotate("C", xy=(-0.05, 1.02), xycoords="axes fraction", fontsize=16)

    return fig, axes


def plot_residual_and_svd(result_datasets: list):
    fig, axes = plt.subplots(1, 3, figsize=(10, 2))
    for result_dataset in result_datasets:
        plot_residual(result_dataset, axes[0])
        plot_lsv_residual(result_dataset, axes[1], indices=[0])
        plot_rsv_residual(result_dataset, axes[2], indices=[0])
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


def plot_svd_of_residual(
    result_dataset,
    result_dataset2,
    result_dataset3,
    result_dataset4,
    linlog,
    linthresh,
    index,
):
    fig, axes = plt.subplots(1, 2, figsize=(10, 2))
    custom_cycler = cycler(color=["tab:grey"])
    plot_lsv_residual(
        result_dataset,
        axes[0],
        indices=[index],
        linlog=linlog,
        linthresh=linthresh,
        cycler=custom_cycler,
    )
    plot_lsv_residual(
        result_dataset2, axes[0], indices=[index], linlog=linlog, linthresh=linthresh
    )
    custom_cycler = cycler(color=["tab:orange"])
    plot_lsv_residual(
        result_dataset3,
        axes[0],
        indices=[index],
        linlog=linlog,
        linthresh=linthresh,
        cycler=custom_cycler,
    )
    custom_cycler = cycler(color=["r"])
    plot_lsv_residual(
        result_dataset4,
        axes[0],
        indices=[index],
        linlog=linlog,
        linthresh=linthresh,
        cycler=custom_cycler,
    )
    axes[0].set_xlabel("Time (ps)")
    axes[0].get_legend().remove()
    axes[0].set_ylabel("")
    axes[0].set_title("residual 1st LSV")
    custom_cycler = cycler(color=["tab:grey"])
    plot_rsv_residual(result_dataset, axes[1], indices=[index], cycler=custom_cycler)
    plot_rsv_residual(result_dataset2, axes[1], indices=[index])
    custom_cycler = cycler(color=["tab:orange"])
    plot_rsv_residual(result_dataset3, axes[1], indices=[index], cycler=custom_cycler)
    custom_cycler = cycler(color=["r"])
    plot_rsv_residual(result_dataset4, axes[1], indices=[index], cycler=custom_cycler)
    axes[1].set_xlabel("Wavelength (nm)")
    axes[1].set_title("residual 1st RSV")
    axes[1].get_legend().remove()
    axes[1].set_ylabel("")

    return fig, axes
