import matplotlib.pyplot as plt
import seaborn as sns
from .utils_stats import fd_bins, tukey_fences

""" Wir verwenden hier .dropna(), da es wir zwischen Darstellung (Plots) und Datenvorbereitung (Imputation & Regeln) unterscheiden. 
    - In utils_plots.py machen wir bewusst s = s.dropna(), weil Plot-Helper-Functions keine fachlischen Entscheidungen über fehlende Werte treffen sollen. Sie sind die Präsentationsschicht.
    - Imputationsstrategien (z.B. gruppenbasierte Median-Imputation) sind in unserer Daten-Pipeline ausgelagert und werden in den Jupyter-Notebooks selbst gehandhabt. Diese verändern unserern Datensatz im data/ folder und sorgen dadurch für Reproduzierbarkeit.
"""

__all__ = ["set_style", "hist_kde", "box_violin", "plot_ecdf", "hist_with_fences"]

def set_style():
    sns.set_context("notebook")
    sns.set_style("whitegrid")

def hist_kde(s, title, unit=None, bw_adjust_list=(0.7,1.0,1.8), save=None):
    s = s.dropna()
    bins = fd_bins(s)
    plt.figure(figsize=(7.2,4.6))
    sns.histplot(s, bins=bins, stat="density", edgecolor="white", alpha=0.35, label=f"Hist (FD={bins})")
    for bw in bw_adjust_list:
        sns.kdeplot(s, bw_adjust=bw, linewidth=2, label=f"KDE bw={bw}")
    _xlabel = f"{title}" + (f" [{unit}]" if unit else "")
    plt.xlabel(_xlabel); plt.ylabel("Dichte"); plt.title(f"{title}: Histogramm + KDE")
    plt.legend(); plt.tight_layout()
    if save: 
        plt.savefig(save, dpi=160)
    plt.show()

def box_violin(s, title, save=None):
    s = s.dropna()
    plt.figure(figsize=(6.6,3.2)); sns.boxplot(x=s, orient="h"); plt.title(f"Boxplot: {title}")
    plt.tight_layout(); 
    if save: plt.savefig(save.replace(".png","_box.png"), dpi=160)
    plt.show()
    plt.figure(figsize=(6.6,3.6)); sns.violinplot(x=s, orient="h", cut=0, inner="quartile"); plt.title(f"Violin: {title}")
    plt.tight_layout(); 
    if save: 
        plt.savefig(save.replace(".png","_violin.png"), dpi=160)
    plt.show()

def plot_ecdf(s, title, unit=None, save=None):
    from .utils_stats import ecdf
    x,y = ecdf(s)
    plt.figure(figsize=(6.4,4)); 
    plt.step(x,y, where="post")
    _xlabel = f"{title}" + (f" [{unit}]" if unit else "")
    plt.xlabel(_xlabel); plt.ylabel("ECDF"); plt.title(f"ECDF: {title}")
    plt.tight_layout()
    if save: 
        plt.savefig(save.replace(".png","_ecdf.png"), dpi=160)
    plt.show()

def hist_with_fences(s, title, unit=None, save=None):
    s = s.dropna()
    bins = fd_bins(s)
    lo,hi = tukey_fences(s,1.5)
    plt.figure(figsize=(7.2,4.2))
    sns.histplot(s, bins=bins, stat="density", edgecolor="white", alpha=0.35)
    plt.axvline(lo, ls="--", lw=2, color="red", label=f"lo={lo:.2f}")
    plt.axvline(hi, ls="--", lw=2, color="red", label=f"hi={hi:.2f}")
    _xlabel = f"{title}" + (f" [{unit}]" if unit else "")
    plt.xlabel(_xlabel); plt.ylabel("Dichte"); plt.title(f"{title}: Hist + Tukey-Grenzen")
    plt.legend()
    plt.tight_layout()
    if save: 
        plt.savefig(save, dpi=160)
    plt.show()