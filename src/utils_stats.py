import numpy as np
import pandas as pd
from scipy.stats import zscore, median_abs_deviation, trim_mean as sp_trim_mean

"""
Design decisions & performance notes
------------------------------------
- Prefer NumPy/SciPy primitives for heavy lifting (quantiles, MAD, z-scores).
- Avoid .dropna() in core computations where possible; use NaN-aware ops
  (np.nanquantile, np.nanmedian, SciPy nan_policy) to *preserve index alignment*.
- Keep helpers *thin* and deterministic. Business rules (imputation etc.) belong
  to the data-prep layer (see project notebooks/pipelines).

Redundant helpers
-----------------
Some functions are provided by Pandas/SciPy already. We keep *thin wrappers* for
API stability and readability, but they could be removed and replaced inline:

- `mad(...)`  ➜ use `scipy.stats.median_abs_deviation(..., scale='normal', nan_policy='omit')`
- `trimmed_mean(...)` ➜ use `scipy.stats.trim_mean(...)`
- `classic_z_score(...)` ➜ use `scipy.stats.zscore(...)` directly

If you prefer, you can call these library functions directly at the call site
and delete the wrappers below.
"""

__all__ = [
    "iqr",
    "mad",
    "trimmed_mean",
    "tukey_fences",
    "tukey_outliers",
    "modified_z_score",
    "ecdf",
    "z_score",
    "create_na_table",
]

# --------------------------------------------------------------------------- #
# Robust summaries
# --------------------------------------------------------------------------- #

def iqr(s: pd.Series) -> float:
    """Interquartile range using NaN-aware NumPy quantiles (fast)."""
    arr = s.to_numpy(dtype="float64", copy=False)
    q1, q3 = np.nanquantile(arr, [0.25, 0.75], method="linear")
    return float(q3 - q1)


def mad(s: pd.Series) -> float:
    """
    Wrapper for SciPy's median absolute deviation. Prefer calling SciPy directly.
    This function exists only for backward-compatibility / readability.
    """
    # NOTE: Could replace all calls with median_abs_deviation(s, scale='normal', nan_policy='omit')
    return float(median_abs_deviation(s.astype(float), scale="normal", nan_policy="omit"))


def trimmed_mean(s: pd.Series, p: float = 0.10) -> float:
    """
    Wrapper for SciPy's trim_mean (proportion p clipped on each side).
    Prefer calling scipy.stats.trim_mean directly.
    """
    # NOTE: sp_trim_mean expects raw array; NaNs propagate. Drop NaNs here explicitly.
    arr = s.to_numpy(dtype="float64", copy=False)
    arr = arr[~np.isnan(arr)]
    return float(sp_trim_mean(arr, proportiontocut=p))


# --------------------------------------------------------------------------- #
# Tukey fences & outliers
# --------------------------------------------------------------------------- #

def tukey_fences(s: pd.Series, k: float = 1.5) -> tuple[float, float]:
    """
    Compute Tukey's lower/upper fences (Q1 - k*IQR, Q3 + k*IQR).
    NaN-aware and fast.
    """
    arr = s.to_numpy(dtype="float64", copy=False)
    q1, q3 = np.nanquantile(arr, [0.25, 0.75], method="linear")
    IQR = q3 - q1
    lower = float(q1 - k * IQR)
    upper = float(q3 + k * IQR)
    return lower, upper


def tukey_outliers(s: pd.Series, k: float = 1.5) -> pd.Series:
    """
    Return a boolean mask (aligned to input index) where True marks Tukey outliers.
    Uses NumPy quantiles for speed. NaN values are not flagged as outliers.
    """
    try:
        if not pd.api.types.is_numeric_dtype(s):
            s = pd.to_numeric(s, errors="raise")

        arr = s.to_numpy(dtype="float64", copy=False)
        lower, upper = tukey_fences(s, k)
        mask = ((arr < lower) | (arr > upper)) & np.isfinite(arr)
        return pd.Series(mask, index=s.index, name=s.name)
    except Exception as e:
        print(f"[tukey_outliers] Error: {e}")
        return pd.Series(False, index=s.index, name=s.name)


def modified_z_score(s: pd.Series, thr: float = 3.5) -> pd.Series:
    """
    Boolean mask for outliers using the robust (median/MAD) z-score.
    Returns False when MAD==0 or undefined.
    """
    s = s.astype(float)
    med = np.nanmedian(s)
    mad_val = np.nanmedian(np.abs(s - med))
    if mad_val == 0 or np.isnan(mad_val):
        return pd.Series(False, index=s.index, name=s.name)
    modz = 0.6745 * (s - med) / mad_val
    return pd.Series(np.abs(modz) > thr, index=s.index, name=s.name)


# ---------------------------------------------------------------------------
# Distributions & diagnostics
# ---------------------------------------------------------------------------

def ecdf(s: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    """
    Empirical CDF. Returns sorted values (x) and cumulative probabilities (y).
    NaNs are removed.
    """
    arr = s.to_numpy(dtype="float64", copy=False)
    arr = arr[~np.isnan(arr)]
    arr.sort(kind="quicksort")
    n = arr.size
    y = np.arange(1, n + 1, dtype="float64") / n
    return arr, y


def z_score(s: pd.Series, threshold: float = 3.0) -> pd.Series:
    zs = zscore(s.astype(float), nan_policy="omit")
    return pd.Series(np.abs(zs) > threshold, index=s.index, name=s.name)


# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------

def create_na_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count and percentage of missing values per column.
    NOTE: This is a simple Pandas composition and could be written inline where used.
    """
    n = len(df)
    out = (
        df.isna()
          .sum()
          .rename("n_missing")
          .reset_index()
          .rename(columns={"index": "column"})
          .assign(percent_missing=lambda x: (x["n_missing"] / n * 100).round(1))
    )
    return out