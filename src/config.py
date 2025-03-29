from enum import Enum, auto
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import os


class SortingType(Enum):
    """
    Enum representing different import sorting strategies.

    Provided predefined sorting types for import statements:
    - FROM_FIRST: Prioritizes 'from' imports
    - IMPORT_FIRST: Prioritizes 'import' imports
    - ALPHABETICAL: Sorts imports alphabetically
    - STRUCTURAL: Sorts by library type (system, third-party, local)
    """

    FROM_FIRST = auto()
    IMPORT_FIRST = auto()
    ALPHABETICAL = auto()
    STRUCTURAL = auto()


class Config(BaseModel):
    """
    Configuration model for import sorter with validation.

    Validates input parameters and provides type safety.
    """

    directory: Optional[str] = Field(
        default=None, description="Directory containing Python files to process"
    )
    file: Optional[str] = Field(default=None, description="Specific file to process")
    sorting_type: SortingType = Field(
        default=SortingType.STRUCTURAL, description="Import sorting strategy to apply"
    )
    verbose: bool = Field(default=False, description="Enable verbose logging")
    dry_run: bool = Field(default=False, description="Enable dry-run")

    @field_validator("directory", "file")
    def validate_path(cls, path):
        """
        Validate that provided paths exist and are accessible.

        Args:
            path (str): File or directory path

        Raises:
            ValueError: If path does not exist or is not readable
        """
        if path and not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")
        return path

    @field_validator("file")
    def validate_file_extension(cls, file):
        """
        Ensure file has a .py extension.

        Args:
            file (str): File path to validate

        Raises:
            ValueError: If file is not a Python file
        """
        if file and not file.endswith(".py"):
            raise ValueError(f"File must be a Python file: {file}")
        return file
