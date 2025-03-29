import ast
from typing import List
from dataclasses import dataclass, field
from enum import Enum, auto


class ImportType(Enum):
    """
    Classify types of import statements.

    Categorizes imports into:
    - SYSTEM: Python standard library imports
    - THIRD_PARTY: External library imports
    - LOCAL: Project-specific imports
    """

    SYSTEM = auto()
    THIRD_PARTY = auto()
    LOCAL = auto()


@dataclass
class ImportStatement:
    """
    Structured representation of a Python import statement.

    Captures details of import statements for further processing.
    """

    original_line: str
    import_type: ImportType
    module: str
    specific_imports: List[str] = field(default_factory=list)
    is_from_import: bool = False


class Parser:
    """
    Parse and categorize import statements from Python source code.
    """

    @staticmethod
    def parse_imports(file_path: str) -> List[ImportStatement]:
        """
        Extract and categorize import statements from a Python file.

        Args:
            file_path (str): Path to the Python file to parse

        Returns:
            List[ImportStatement]: Parsed and categorized import statements
        """
        try:
            with open(file_path, "r") as file:
                tree = ast.parse(file.read())

        except (IOError, SyntaxError) as e:
            raise ValueError(f"Error parsing file {file_path}: {e}")

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(Parser._create_import_statement(alias.name))

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(
                        Parser._create_from_import_statement(module, alias.name)
                    )

        return imports

    @staticmethod
    def _create_import_statement(module: str) -> ImportStatement:
        """
        Create an import statement for standard 'import' syntax.

        Args:
            module (str): Module name to import

        Returns:
            ImportStatement: Parsed import statement
        """
        import_type = Parser._classify_import_type(module)
        return ImportStatement(
            original_line=f"import {module}",
            import_type=import_type,
            module=module,
            is_from_import=False,
        )

    @staticmethod
    def _create_from_import_statement(
        module: str, specific_import: str
    ) -> ImportStatement:
        """
        Create an import statement for 'from ... import ...' syntax.

        Args:
            module (str): Source module
            specific_import (str): Specific item being imported

        Returns:
            ImportStatement: Parsed from-import statement
        """
        import_type = Parser._classify_import_type(module)
        return ImportStatement(
            original_line=f"from {module} import {specific_import}",
            import_type=import_type,
            module=module,
            specific_imports=[specific_import],
            is_from_import=True,
        )

    @staticmethod
    def _classify_import_type(module: str) -> ImportType:
        """
        Classify import type based on module name.

        Args:
            module (str): Module name to classify

        Returns:
            ImportType: Categorized import type
        """
        # Standard library check (simplistic approach)
        standard_libs = ["os", "re", "sys", "math", "json", "datetime"]

        if any(module.startswith(lib) for lib in standard_libs):
            return ImportType.SYSTEM

        # Local project import (contains no dots or starts with current project)
        if "." not in module or module.startswith("."):
            return ImportType.LOCAL

        return ImportType.THIRD_PARTY
