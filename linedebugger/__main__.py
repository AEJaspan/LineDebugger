import argparse

from .linedebugger import debug_script


def main() -> None:
    """Runs the script."""
    parser = argparse.ArgumentParser(
        description="Run a Python script with line-by-line debugging."
    )
    parser.add_argument(
        "-p",
        "--script_path",
        default="example_script.py",
        help="Path to the Python script to debug",
    )
    parser.add_argument(
        "-o", "--output", default="debug_log.md", help="Path to save the debug log"
    )
    args = parser.parse_args()

    debug_script(script=args.script_path, output=args.output)


if __name__ == "__main__":
    main()
