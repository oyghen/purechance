import purechance_cli


def main():
    result = purechance_cli.__name__
    expected = "purechance_cli"
    if result == expected:
        print(f"Smoke test for {purechance_cli.__name__}: PASSED")
    else:
        raise RuntimeError(f"Smoke test for {purechance_cli.__name__}: FAILED")


if __name__ == "__main__":
    main()
