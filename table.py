import math
from itertools import combinations
from typing import List, Tuple, Any
import codetotable as mml

class MMLCalculator:
    def __init__(self, tabletotal: int, attributes: int, unique_counts: List[int], rows: int):
        self.tabletotal = tabletotal
        self.attributes = attributes
        self.unique_counts = unique_counts
        self.rows = rows

    def calculate_H(self, tables: List[Tuple[int, int]]) -> float:
        return mml.H(self.tabletotal, self.attributes, tables)
    
    def calculate_A(self, data: List[Tuple[int, List[int]]]) -> float:
        return mml.A(data)
    
    def calculate_I(self, tables: List[Tuple[int, int]], data: List[Tuple[int, List[int]]]) -> float:
        return mml.I(self.tabletotal, self.attributes, tables, data)
    
    def calculate_mml_for_combination(self, comb: Tuple[int, ...], total_columns: int) -> float:
        tables = [(total_columns, len(comb))]
        data = [(self.rows, self.unique_counts)]
        return self.calculate_I(tables, data)

class Table:
    def __init__(self, table_data: List[List[Any]]):
        self.table_data = table_data
        self.header = table_data[0]
        self.rows = table_data[1:]
        self.unique_counts = self._count_unique_instances_per_column()
        # Currently hardcoded to 1 table, must change later for further NFs
        self.mml_calculator = MMLCalculator(1, len(self.header), self.unique_counts, len(self.rows))
        
    """Generate all possible combinations of given columns."""
    def _get_combinations(self, columns: List[str]) -> List[Tuple[int, ...]]:
        col_indices = [self.header.index(col) for col in columns]
        return list(combinations(col_indices, len(columns)))
    
    """Check if the given combination of column indices has unique values for all rows."""
    def _is_unique_combination(self, combination: Tuple[int, ...]) -> bool:
        seen = set()
        for row in self.rows:
            key = tuple(row[i] for i in combination)
            if key in seen:
                return False
            seen.add(key)
        return True
    
    """Count the number of unique instances for each column."""
    def _count_unique_instances_per_column(self) -> List[int]:
        unique_counts = []
        for col_index in range(len(self.header)):
            unique_values = set(row[col_index] for row in self.rows)
            unique_counts.append(len(unique_values))
        return unique_counts

    """Generate all valid combinations of columns as primary keys."""
    def get_valid_primary_key_combinations(self) -> List[Tuple[str, ...]]:
        num_columns = len(self.header)
        valid_combinations = []
        for r in range(1, num_columns + 1):
            for comb in combinations(range(num_columns), r):
                if self._is_unique_combination(comb):
                    valid_combinations.append(tuple(self.header[i] for i in comb))
        return valid_combinations
    
    """Display the table."""
    def display_table(self) -> None:
        for row in self.table_data:
            print('\t'.join(map(str, row)))
    
    """Calculate MML for all valid primary key combinations and return the one with the shortest MML."""
    def calculate_mml_for_combinations(self) -> Tuple[Tuple[str, ...], float]:
        valid_combinations = self.get_valid_primary_key_combinations()
        best_combination = None
        best_mml = float('inf')
        
        for comb in valid_combinations:
            mml_value = self.mml_calculator.calculate_mml_for_combination(comb, len(self.header))
            # Break MML tiebreaks with the lowest number of attributes in primary key
            if mml_value < best_mml or (mml_value == best_mml and (best_combination is None or len(comb) < len(best_combination))):
                best_mml = mml_value
                best_combination = comb
        
        return best_combination, best_mml

# Example usage:
table_data: List[List[Any]] = [
    ["id", "name", "age", "city"],
    [1, "Alice", 30, "New York"],
    [2, "Bob", 25, "Los Angeles"],
    [3, "Charlie", 35, "Chicago"],
    [4, "Charlie", 23, "Las Vegas"],
    [5, "Alice", 30, "Chicago"]
]

table = Table(table_data)
table.display_table()

valid_primary_key_combinations: List[Tuple[str, ...]] = table.get_valid_primary_key_combinations()
print("All valid combinations of primary keys:")
for comb in valid_primary_key_combinations:
    print(comb)

print("Unique instances per column:", table.unique_counts)

best_combination, best_mml = table.calculate_mml_for_combinations()
print(f"Best combination for primary key: {best_combination} with MML: {best_mml}")
