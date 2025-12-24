import purechance


def main():
    result = purechance.__name__
    expected = "purechance"
    if result == expected:
        print("smoke test passed")
    else:
        raise RuntimeError("smoke test failed")


if __name__ == "__main__":
    main()
