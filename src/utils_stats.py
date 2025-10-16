import numpy as np
import pandas as pd

"""
Design-Entscheidung: Missing-Handling in zwei Schichten trennen.

1) Datenvorbereitung (Pipelines/Notebooks):
   - Imputation/Regeln (z. B. gruppenbasierte Median-/Quantil-Imputation nach payment_type, Stunde, etc.)
   - Output als neue, versionierte Artefakte (z. B. data/processed/*.parquet) – Raw-Daten bleiben unverändert.
   - Reproduzierbarkeit über DVC (Stages/Deps).

2) Helper (dieses Modul & utils_plots):
   - Treffen KEINE fachlichen Imputationsentscheidungen.
   - Arbeiten standardmäßig mit gültigen Werten und verwenden daher .dropna().
   - Ziel: neutrale, reproduzierbare Berechnungen/Plots ohne implizite Ersetzungen.

Konsequenz:
- Imputation gehört in die Prep-Schicht (Notebook/Pipeline), nicht in die Helper.
- Für Varianz/SD in Notebooks ddof=1 (Stichprobe), robuste Maße (Median, IQR, MAD) zuerst berichten – vgl. Slides SDS-02A.
"""

__all__ = ["iqr", "mad", "trimmed_mean", "fd_bins", "tukey_fences", "modified_z_scores", "ecdf"]

def iqr(x: pd.Series) -> float:
    x = x.dropna(); q = x.quantile([.25,.75])
    return float(q.iloc[1] - q.iloc[0])

def mad(x: pd.Series) -> float:
    x = x.dropna(); m = x.median()
    return float((x - m).abs().median())

def trimmed_mean(x: pd.Series, p=0.10) -> float:
    x = x.dropna(); lo,hi = x.quantile([p,1-p])
    return float(x[(x >= lo) & (x <= hi)].mean())

def fd_bins(x: pd.Series) -> int:
    x = x.dropna(); n = x.size
    if n<2: return 10
    I = iqr(x)
    h = 2*I / (n ** (1/3)) if I>0 else 0
    if h<=0: 
        return 10
    b = int(np.ceil((x.max()-x.min())/h))
    return b if b > 1 else 10

def tukey_fences(x: pd.Series, k=1.5):
    x = x.dropna(); q1,q3 = x.quantile([.25,.75]); I = q3-q1
    return float(q1 - k * I), float(q3 + k * I)

def modified_z_scores(x: pd.Series) -> pd.Series:
    x = x.dropna(); M = x.median(); MAD = mad(x)
    if MAD==0: return pd.Series(np.zeros_like(x), index=x.index, dtype=float)
    return 0.6745 * (x - M)/MAD

def ecdf(x: pd.Series):
    x = x.dropna().sort_values()
    y = np.arange(1, len(x) + 1)/len(x)
    return x.values, y