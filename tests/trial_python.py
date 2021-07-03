from tools import synth_set, linestrings_py

def main(count=2_000_000):
    args = synth_set(bound_lower=count - 1, bound_upper=count) + (2,)
    actual = linestrings_py(*args)
    print(f"Finished with {len(actual)}")


if __name__ == "__main__":
    main()
