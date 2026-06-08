import litexpy


def main():
    code = """
forall x R:
    x = 2
    =>:
        x + 1 = 3
        x^2 = 4
"""

    runner = litexpy.Runner()
    try:
        results = runner.run(code)
        for result in results:
            print(result)
    finally:
        runner.quit()


if __name__ == "__main__":
    main()
