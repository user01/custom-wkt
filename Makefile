
large:
	cargo build
	maturin build --release --no-sdist -i python3.9
	pip install --force-reinstall target/wheels/custom_wkt-0.1.0-cp39-cp39-manylinux_2_24_x86_64.whl
	pytest -x -rws -vv tests/test_*  --benchmark-histogram

small:
	cargo build
	maturin build --release --no-sdist -i python3.9
	pip install --force-reinstall target/wheels/custom_wkt-0.1.0-cp39-cp39-manylinux_2_24_x86_64.whl
	pytest -x -rws -vv tests/test_logic.py tests/test_benchmark_small.py

logic:
	cargo build
	maturin build --release --no-sdist -i python3.9
	pip install --force-reinstall target/wheels/custom_wkt-0.1.0-cp39-cp39-manylinux_2_24_x86_64.whl
	pytest -x -rws -vv tests/test_logic.py

memory:
	rm *.dat
	mprof run --output res_python.dat tests/trial_python.py
	mprof plot --output .github/plot_python.svg --flame --slope --title "Python Version Memory" res_python.dat

	mprof run --output res_pandas.dat tests/trial_pandas.py
	mprof plot --output .github/plot_pandas.svg --flame --slope --title "Pandas Version Memory" res_pandas.dat

	mprof run --output res_rust.dat tests/trial_rust.py
	mprof plot --output .github/plot_rust.svg --flame --slope --title "Rust Version Memory" res_rust.dat
