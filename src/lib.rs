mod linestring;

use numpy::PyArrayDyn;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::Python;

/// Returns a Python List of string representations
///
/// # Arguments
///
/// * `x` - Reference to a 1D float64 numpy array of length N - X Position
/// * `y` - Reference to a 1D float64 numpy array of length N - Y Position
/// * `classes` - Reference to a 1D int16 numpy array of length N - IDs. Must be ordered and correspond to points
/// * `precision` - usize (pointer-sized unsigned integer type) for precision of WKT rendering
///
#[pyfunction]
fn linestring(
    x: &PyArrayDyn<f64>,
    y: &PyArrayDyn<f64>,
    classes: &PyArrayDyn<i64>,
    precision: usize,
) -> PyResult<Vec<String>> {
    let x = unsafe { x.as_array().to_owned() };
    let y = unsafe { y.as_array().to_owned() };
    let classes = unsafe { classes.as_array().to_owned() };

    {
        let dims_x = x.shape().len();
        if dims_x != 1 {
            Err(PyValueError::new_err(format!(
                "Expected 1d array for x, but found {}",
                dims_x
            )))?;
        }
    }
    {
        let dims_y = y.shape().len();
        if dims_y != 1 {
            Err(PyValueError::new_err(format!(
                "Expected 1d array for y, but found {}",
                dims_y
            )))?;
        }
    }
    {
        let dims_classes = classes.shape().len();
        if dims_classes != 1 {
            Err(PyValueError::new_err(format!(
                "Expected 1d array for classes, but found {}",
                dims_classes
            )))?;
        }
    }
    let length_a = *x.shape().first().unwrap();
    let length_b = *y.shape().first().unwrap();
    let length_classes = *classes.shape().first().unwrap();
    if length_a != length_classes || length_a != length_classes {
        Err(PyValueError::new_err(format!(
            "Array lengths mismatch {} {} {}",
            length_a, length_b, length_classes
        )))?;
    }
    if length_a < (2 as usize) {
        Err(PyValueError::new_err(format!(
            "Insufficient array length {}",
            length_a
        )))?;
    }
    let mut results = Vec::new();
    let mut tail = 0usize;
    let mut tag = classes[0];
    for lead in 0..length_a {
        let write_required = tag != classes[lead];

        if write_required {
            // this write is inclusive of this range
            let result = linestring::render_into_linestring(lead, tail, &x, &y, precision);
            results.push(result);
            tail = lead;
            tag = classes[lead];
        }
    }

    // Close last grouping write
    let result = linestring::render_into_linestring(length_a, tail, &x, &y, precision);
    results.push(result);

    Ok(results)
}

/// A Python module implemented in Rust to convert floating point data
/// to WKT strings
#[pymodule]
fn custom_wkt(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(linestring, m)?)?;

    Ok(())
}
