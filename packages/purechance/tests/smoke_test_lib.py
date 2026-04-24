import purechance


def main() -> None:
    result = purechance.__name__
    expected = "purechance"
    if result == expected:
        print(f"Smoke test for {purechance.__name__}: PASSED")
    else:
        raise RuntimeError(f"Smoke test for {purechance.__name__}: FAILED")


if __name__ == "__main__":
    main()
