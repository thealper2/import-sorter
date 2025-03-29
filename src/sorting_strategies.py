from typing import List
from import_parser import ImportStatement, ImportType
from config import SortingType


class Sorter:
    """
    Provides strategies for sorting import statements.
    """

    @staticmethod
    def sort_imports(
        imports: List[ImportStatement], sorting_type: SortingType
    ) -> List[ImportStatement]:
        """
        Sort import statements based on specified strategy.

        Args:
            imports (List[ImportStatement]): List of import statements
            sorting_type (SortingType): Sorting strategy to apply

        Returns:
            List[ImportStatement]: Sorted import statements
        """
        strategy_map = {
            SortingType.FROM_FIRST: Sorter._from_first_sort,
            SortingType.IMPORT_FIRST: Sorter._import_first_sort,
            SortingType.ALPHABETICAL: Sorter._alphabetical_sort,
            SortingType.STRUCTURAL: Sorter._structural_sort,
        }

        return strategy_map[sorting_type](imports)

    @staticmethod
    def _from_first_sort(imports: List[ImportStatement]) -> List[ImportStatement]:
        """
        Sort imports with 'from' imports first.

        Args:
            imports (List[ImportStatement]): Unsorted import statements

        Returns:
            List[ImportStatement]: Sorted import statements
        """
        return sorted(imports, key=lambda x: (not x.is_from_import, x.original_line))

    @staticmethod
    def _import_first_sort(imports: List[ImportStatement]) -> List[ImportStatement]:
        """
        Sort imports with standard 'import' statements first.

        Args:
            imports (List[ImportStatement]): Unsorted import statements

        Returns:
            List[ImportStatement]: Sorted import statements
        """
        return sorted(imports, key=lambda x: (x.is_from_import, x.original_line))

    @staticmethod
    def _alphabetical_sort(imports: List[ImportStatement]) -> List[ImportStatement]:
        """
        Sort imports alphabetically by original line.

        Args:
            imports (List[ImportStatement]): Unsorted import statements

        Returns:
            List[ImportStatement]: Sorted import statements
        """
        return sorted(imports, key=lambda x: x.original_line)

    @staticmethod
    def _structural_sort(imports: List[ImportStatement]) -> List[ImportStatement]:
        """
        Sort imports by library type: system, third-party, local.

        Args:
            imports (List[ImportStatement]): Unsorted import statements

        Returns:
            List[ImportStatement]: Sorted import statements
        """
        type_order = {
            ImportType.SYSTEM: 0,
            ImportType.THIRD_PARTY: 1,
            ImportType.LOCAL: 2,
        }

        return sorted(
            imports, key=lambda x: (type_order[x.import_type], x.original_line)
        )
