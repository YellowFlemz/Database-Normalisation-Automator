import math
from itertools import combinations
from typing import List, Tuple, Any
import codetotable as mml
import util

class Table:

    def __init__(self, table_data: List[List[Any]]):
        self.table_data = table_data
        self.keys = util.remove_asterisks(table_data[0])
        self.key_count = len(self.keys)
        # Primary keys are indicated with an asterisk (*) at the end of the key name upon initialisation
        # However, asterisks are removed from all key lists after initialisation
        self.primary_keys = util.remove_asterisks([key for key in table_data[0] if key[-1] == "*"])
        self.non_primary_keys = [key for key in table_data[0] if key not in self.primary_keys]
        self.primary_key_count = len(self.primary_keys)
        self.rows = table_data[1:]
        self.unique_counts = self._count_unique_instances_per_column()

    def get_key_column(self, key: str) -> List[Any]:
        key_index = self.keys.index(key)
        return [row[key_index] for row in self.rows]

    """Count the number of unique instances for each column."""
    def _count_unique_instances_per_column(self) -> List[int]:
        unique_counts = []
        for col_index in range(len(self.keys)):
            # set() removes duplicates
            unique_values = set(row[col_index] for row in self.rows)
            unique_counts.append(len(unique_values))
        return unique_counts

    """Check if the given combination of column indices has unique values for all rows."""
    def _is_unique_combination(self, combination: Tuple[int, ...]) -> bool:
        seen = set()
        for row in self.rows:
            # subset is the values in the row at the specified indices
            # e.g. row = (1, "Alice", 30, "New York"), combination = (0, 1, 2)
            # subset = (1, "Alice", 30)
            subset = tuple(row[i] for i in combination)
            if subset in seen:
                return False
            seen.add(subset)
        return True

    """Generate all valid combinations of columns as primary keys."""
    def get_valid_primary_key_combinations(self) -> List[Tuple[str, ...]]:
        num_columns = len(self.keys)
        valid_combinations = []
        for r in range(1, num_columns + 1):
            # combinatorics to get all combinations of r columns
            for comb in combinations(range(num_columns), r):
                if self._is_unique_combination(comb):
                    valid_combinations.append(tuple(self.keys[i] for i in comb))
        return valid_combinations
    
    """
    Calculate MML for all valid primary key combinations and return the one with the shortest MML.
    """
    def calculate_best_primary_keys(self) -> Tuple[Tuple[str, ...], float]:
        valid_combinations = self.get_valid_primary_key_combinations()
        best_combination = None
        best_mml = float('inf')
        
        for comb in valid_combinations:
            # Calculates the MML value for the current combination
            mml_value = mml.I(1, self.key_count, [(self.key_count, len(comb))], [(len(self.rows), self.unique_counts)])
            # Break MML tiebreaks with the lowest number of attributes in primary key
            if mml_value < best_mml or (mml_value == best_mml and (best_combination is None or len(comb) < len(best_combination))):
                best_mml = mml_value
                best_combination = comb
        
        return best_combination, best_mml

    """Display the table."""
    def display_table(self) -> None:
        for row in self.table_data:
            print('\t'.join(map(str, row)))
