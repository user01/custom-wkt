import custom_wkt
import pytest

from .tools import linestrings_py, linestrings_pd, synth_set


@pytest.mark.benchmark(group="large-points")
def test_rust_version_large(benchmark):
    args = synth_set(bound_lower=200_000 - 1, bound_upper=200_000) + (2,)
    actual = benchmark.pedantic(custom_wkt.linestring, args=args, warmup_rounds=2, rounds=15, iterations=15)
    expected = linestrings_py(*args)
    assert len(actual) == len(expected)
    for a, e in zip(actual, expected):
        assert a == e


@pytest.mark.benchmark(group="large-points")
def test_py_version_large(benchmark):
    args = synth_set(bound_lower=200_000 - 1, bound_upper=200_000) + (2,)
    actual = benchmark.pedantic(linestrings_py, args=args, warmup_rounds=2, rounds=15, iterations=15)
    expected = linestrings_py(*args)
    assert len(actual) == len(expected)
    for a, e in zip(actual, expected):
        assert a == e


@pytest.mark.benchmark(group="large-points")
def test_pd_version_large(benchmark):
    args = synth_set(bound_lower=200_000 - 1, bound_upper=200_000) + (2,)
    _ = benchmark.pedantic(linestrings_pd, args=args, warmup_rounds=2, rounds=15, iterations=15)
