from typing import List, Tuple
from itertools import groupby
import numpy as np
import pandas as pd


def synth_set(seed=451, bound_lower=5, bound_upper=200):
    rs = np.random.RandomState(seed)
    count = rs.randint(bound_lower, bound_upper)

    xs = rs.randn(count).astype(np.float64)
    ys = rs.randn(count).astype(np.float64)
    classes = np.cumsum(rs.rand(count) > 0.85).astype(np.int64)

    return xs, ys, classes


def linestrings_py(x: np.ndarray, y: np.ndarray, classes: np.ndarray, precision: int) -> List[str]:
    """Python Implementation for consolidation

    Parameters
    ----------
    x : np.ndarray
        First Point Value - float64
    y : np.ndarray
        Second Point Values - float64
    classes : np.ndarray
        Classes - int64
    precision : int
        Number of places for rendering in string, >= 0

    Returns
    -------
    List[str]
        List of LineStrings
    """
    assert x.dtype == np.float64
    assert y.dtype == np.float64
    assert classes.dtype == np.int64
    assert isinstance(precision, int)
    assert precision >= 0
    results = []
    data = list(zip(x.tolist(), y.tolist(), classes.tolist()))
    groups = groupby(data, key=lambda i: i[2])
    for _, group in groups:
        results.append(_linestring_py(list(group), precision=precision))
    return results


def _linestring_py(data: List[Tuple[float, float, int]], precision: int) -> List[str]:
    return "LINESTRING (" + ", ".join([f"{d[0]:.{precision}f} {d[1]:.{precision}f}" for d in data]) + ")"


def linestrings_pd(x: np.ndarray, y: np.ndarray, classes: np.ndarray, precision: int) -> List[str]:
    """Pandas Implementation for consolidation

    NOTE: Due to formatting differences with the round() call, these results are functionally identical
    but do not match as strings (trailing zeros do not exist in this solution)

    Parameters
    ----------
    x : np.ndarray
        First Point Value - float64
    y : np.ndarray
        Second Point Values - float64
    classes : np.ndarray
        Classes - int64
    precision : int
        Number of places for rendering in string, >= 0

    Returns
    -------
    List[str]
        List of LineStrings
    """
    assert x.dtype == np.float64
    assert y.dtype == np.float64
    assert classes.dtype == np.int64
    assert isinstance(precision, int)
    assert precision >= 0
    result = (
        pd.DataFrame({"x": x, "y": y, "classes": classes})
        .assign(
            element=lambda idf: idf["x"].round(precision).astype(str) + " " + idf["y"].round(precision).astype(str)
        )
        .groupby("classes")
        .agg(", ".join)[["element"]]
        .assign(WKT=lambda idf: "LINESTRING (" + idf["element"] + ")")["WKT"]
        .tolist()
    )
    return result
