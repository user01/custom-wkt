from custom_wkt import linestring
from tools import synth_set

def main(count=2_000_000):
    args = synth_set(bound_lower=count - 1, bound_upper=count) + (2,)
    actual = linestring(*args)
    print(f"Finished with {len(actual)}")


if __name__ == "__main__":
    main()
