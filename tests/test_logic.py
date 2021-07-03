import numpy as np
import custom_wkt
import pytest

from .tools import linestrings_py, synth_set


@pytest.fixture
def data():
    xs = [0, 1, 1, 0, 3, 4, 4, 3, 5, 6, 5.5, 9, 99]
    ys = [0, 0, 1, 1, 3, 3, 4, 4, 1, 1, 3, 10, 11]
    classes = ([0] * 4) + ([1] * 4) + ([2] * 3) + ([3] * 2)
    return (
        np.array(xs).astype(np.float64),
        np.array(ys).astype(np.float64),
        np.array(classes).astype(np.int64),
    )


def test_python_exception(data):
    # Test python exceptions from Rust are raised
    xs, ys, classes = data
    with pytest.raises(ValueError) as excinfo:
        _ = custom_wkt.linestring(
            xs[:-1],
            ys,
            classes,
            precision=3,
        )
    assert "Array lengths mismatch 12 13 13" in str(excinfo.value)


def test_basic_operation(data):
    # Test python exceptions from Rust are raised
    xs, ys, classes = data

    result = custom_wkt.linestring(
        xs,
        ys,
        classes,
        precision=2,
    )
    assert result == [
        "LINESTRING (0.00 0.00, 1.00 0.00, 1.00 1.00, 0.00 1.00)",
        "LINESTRING (3.00 3.00, 4.00 3.00, 4.00 4.00, 3.00 4.00)",
        "LINESTRING (5.00 1.00, 6.00 1.00, 5.50 3.00)",
        "LINESTRING (9.00 10.00, 99.00 11.00)",
    ]


def test_precision(data):
    # Test python exceptions from Rust are raised
    xs, ys, classes = data

    result = custom_wkt.linestring(
        xs[:4],
        ys[:4],
        classes[:4],
        precision=1,
    )
    assert len(result) == 1
    assert result[0] == "LINESTRING (0.0 0.0, 1.0 0.0, 1.0 1.0, 0.0 1.0)"


def test_named_arguments(data):
    # Test python named arguments are allowed
    xs, ys, classes = data

    result = custom_wkt.linestring(
        x=xs[:4],
        y=ys[:4],
        classes=classes[:4],
        precision=1,
    )
    assert len(result) == 1
    assert result[0] == "LINESTRING (0.0 0.0, 1.0 0.0, 1.0 1.0, 0.0 1.0)"


def test_precision_0(data):
    # Test python exceptions from Rust are raised
    xs, ys, classes = data

    result = custom_wkt.linestring(
        xs[:4],
        ys[:4],
        classes[:4],
        precision=0,
    )
    assert len(result) == 1
    assert result[0] == "LINESTRING (0 0, 1 0, 1 1, 0 1)"


def test_compare_to_py(data):
    # against python version
    xs, ys, classes = data

    expected = linestrings_py(
        xs[:4],
        ys[:4],
        classes[:4],
        precision=1,
    )
    actual = custom_wkt.linestring(
        xs[:4],
        ys[:4],
        classes[:4],
        precision=1,
    )
    assert len(actual) == len(expected)
    assert actual[0] == expected[0]
    assert len(actual) == 1


def test_many_examples():
    for seed in range(20):
        _compare_to_py(*synth_set(seed=seed))


def _compare_to_py(xs, ys, classes):
    expected = linestrings_py(
        xs,
        ys,
        classes,
        precision=1,
    )
    actual = custom_wkt.linestring(
        xs,
        ys,
        classes,
        precision=1,
    )
    assert len(actual) == len(expected)
    for a, e in zip(actual, expected):
        assert a == e
