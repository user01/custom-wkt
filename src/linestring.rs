/// Produces a WKT LINESTRING representations of a series of 2d points
///
/// # Arguments
///
/// * `lead` - Start index in array for this LINESTRING
/// * `tail` - End index in array for this LINESTRING
/// * `points_a` - Reference to a 1D float64 numpy array of length N - X Position
/// * `points_b` - Reference to a 1D float64 numpy array of length N - Y Position
/// * `precision` - usize (pointer-sized unsigned integer type) for precision of WKT rendering
///
pub fn render_into_linestring(
    lead: usize,
    tail: usize,
    points_a: &ndarray::ArrayBase<ndarray::OwnedRepr<f64>, ndarray::Dim<ndarray::IxDynImpl>>,
    points_b: &ndarray::ArrayBase<ndarray::OwnedRepr<f64>, ndarray::Dim<ndarray::IxDynImpl>>,
    precision: usize,
) -> String {
    // LINESTRING (0.00 0.00, 1.00 0.00, 1.00 1.00, 0.00 1.00)
    let mut s = String::with_capacity(13 + (10 + precision) * (lead - tail));

    let mut v = vec!["LINESTRING (".to_string()];
    for position in tail..lead {
        let item = format!(
            "{:.precision$} {:.precision$}",
            points_a[position],
            points_b[position],
            precision = precision
        );
        v.push(item);

        if position >= lead - 1 {
            v.push(")".to_string());
        } else {
            v.push(", ".to_string());
        };
    }
    s.extend(v);
    s
}

#[cfg(test)]
mod tests {
    use super::*;
    use ndarray::prelude::*;

    #[test]
    fn basic_op() {
        let a = array![1., 1., 2., 2.].into_dyn();
        let b = array![0., 5., 0., 5.].into_dyn();
        let result = render_into_linestring(2, 0, &a, &b, 2);
        assert_eq!(result, "LINESTRING (1.00 0.00, 1.00 5.00)".to_string());
    }

    #[test]
    fn single_element() {
        let a = array![1., 1., 2., 2.].into_dyn();
        let b = array![0., 5., 0., 5.].into_dyn();
        let result = render_into_linestring(1, 0, &a, &b, 2);
        assert_eq!(result, "LINESTRING (1.00 0.00)".to_string());
    }

    #[test]
    fn last_element() {
        let a = array![1., 1., 2., 2.].into_dyn();
        let b = array![0., 5., 0., 5.].into_dyn();
        let result = render_into_linestring(4, 3, &a, &b, 2);
        assert_eq!(result, "LINESTRING (2.00 5.00)".to_string());
    }

    #[test]
    fn basic_precision() {
        let a = array![1., 1., 2., 2.].into_dyn();
        let b = array![0., 5., 0., 5.].into_dyn();
        let result = render_into_linestring(2, 0, &a, &b, 5);
        assert_eq!(
            result,
            "LINESTRING (1.00000 0.00000, 1.00000 5.00000)".to_string()
        );
    }

    #[test]
    fn basic_op_all() {
        let a = array![1., 1., 2., 2.].into_dyn();
        let b = array![0., 5., 0., 5.].into_dyn();
        let result = render_into_linestring(4, 0, &a, &b, 2);
        assert_eq!(
            result,
            "LINESTRING (1.00 0.00, 1.00 5.00, 2.00 0.00, 2.00 5.00)".to_string()
        );
    }
}
