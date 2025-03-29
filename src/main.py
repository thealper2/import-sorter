import os
import sys
import logging
from typing import List, Optional

from config import Config, SortingType
from import_parser import Parser
from sorting_strategies import Sorter
from utils import setup_argparser


class ImportSorter:
    """
    Main application for sorting Python import statements.

    Handles command-line argument parsing, file processing,
    and import statement sorting.
    """

    def __init__(self):
        """
        Initialize the Import Sorter application.

        Sets up logging and prepares for import sorting operations.
        """
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def run(self, args: Optional[List[str]] = None):
        """
        Main entry point for the import sorting application.

        Args:
            args (Optional[List[str]]): Command-line arguments
        """
        try:
            config = self._parse_arguments(args)
            self._process_files(config)

        except Exception as e:
            self.logger.error(f"Error during import sorting: {e}")
            sys.exit(1)

    def _parse_arguments(self, args: Optional[List[str]] = None) -> Config:
        """
        Parse command-line arguments and create configuration.

        Args:
            args (Optional[List[str]]): Command-line arguments

        Returns:
            Config: Validated configuration object
        """
        parser = setup_argparser()
        parsed_args = parser.parse_args(args)

        config = Config(
            directory=parsed_args.directory,
            file=parsed_args.file,
            sorting_type=SortingType[parsed_args.type.upper()],
            verbose=parsed_args.verbose,
            dry_run=parsed_args.dry_run,
        )

        return config

    def _process_files(self, config: Config):
        """
        Process Python files based on configuration.

        Args:
            config (Config): Configuration for file processing
        """
        if config.file:
            self._process_single_file(config.file, config)

        elif config.directory:
            self._process_directory(config.directory, config)

        else:
            raise ValueError("Either --file or --directory must be specified")

    def _process_single_file(self, file_path: str, config: Config):
        """
        Process and sort imports for a single file.

        Args:
            file_path (str): Path to the Python file
            config (Config): Sorting configuration
        """
        try:
            # Read the entire file content
            with open(file_path, "r") as file:
                content = file.readlines()

            # Seperate import statements
            import_statements = []
            non_import_content = []
            for line in content:
                stripped_line = line.strip()
                if stripped_line.startswith(("import ", "from ")):
                    import_statements.append(line)
                else:
                    non_import_content.append(line)

            # Parse and sort imports
            parsed_imports = Parser.parse_imports(file_path)
            sorted_imports = Sorter.sort_imports(parsed_imports, config.sorting_type)

            # Convert sorted imports back to lines
            sorted_import_lines = [imp.original_line + "\n" for imp in sorted_imports]

            # Combine sorted imports with rest of the content
            new_content = sorted_import_lines + non_import_content

            # Verbose logging
            if config.verbose:
                self.logger.info(f"Processing file: {file_path}")
                self.logger.info("Original imports:")
                for imp in import_statements:
                    self.logger.info(imp[:-1])

                self.logger.info("Sorted imports:")
                for imp in sorted_import_lines:
                    self.logger.info(imp[:-1])

            # Write changes
            if not config.dry_run:
                with open(file_path, "w") as file:
                    file.writelines(new_content)
                self.logger.info(f"Successfully sorted imports in {file_path}")

        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")

    def _process_directory(self, directory: str, config: Config):
        """
        Process and sort imports for all Python files in a directory.

        Args:
            directory (str): Directory path
            config (Config): Sorting configuration
        """
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        self._process_single_file(file_path, config)
                    except Exception as e:
                        self.logger.error(f"Error processing {file_path}: {e}")


def main():
    """
    Entry point for the import sorter application.
    """
    app = ImportSorter()
    app.run()


if __name__ == "__main__":
    main()
