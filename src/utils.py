import argparse

from config import SortingType


def setup_argparser() -> argparse.ArgumentParser:
    """
    Sets command line arguments.

    Returns:
        argparse.ArgumentParser: Argument parser
    """
    parser = argparse.ArgumentParser(description="Python Import Statement Sorter")
    parser.add_argument(
        "--directory", help="Directory containing Python files to process"
    )
    parser.add_argument("--file", help="Specific Python file to process")
    parser.add_argument(
        "--type",
        choices=[t.name.lower() for t in SortingType],
        default=SortingType.STRUCTURAL.name.lower(),
        help="Import sorting strategy",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without modifying files"
    )
    return parser
