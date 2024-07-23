from __future__ import annotations
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
        # However, asterisks are removed from all key lists after initialisation (EXCEPT in table_data[0])
        self.primary_keys = util.remove_asterisks([key for key in table_data[0] if key[-1] == "*"])
        self.non_primary_keys = [key for key in table_data[0] if key[-1] != "*"]
        self.primary_key_count = len(self.primary_keys)
        self.rows = table_data[1:]
        # Important: Automatically removes duplicate rows upon initialisation
        self.remove_duplicate_rows()
        self.unique_counts = self._count_unique_instances_per_column()
        self.candidate_keys = self.calculate_candidate_keys()
        self.prime_attributes = self.calculate_prime_attributes()
        self.non_prime_attributes = self.calculate_non_prime_attributes()

    """Get all values of a key in the table."""
    def get_key_column(self, key: str) -> List[Any]:
        key_index = self.keys.index(key)
        return [row[key_index] for row in self.rows]
    
    """
    Remove a key and its corresponding values from the table.
    Note: Do not pass in primary keys with asterisks (e.g. "studentNo*" should be passed as "studentNo")
    """
    def remove_key_column(self, key: str) -> None:
        key_index = self.keys.index(key)
        for row in self.rows:
            del row[key_index]
        self.keys.remove(key)
        if key in self.primary_keys:
            self.primary_keys.remove(key)
            self.primary_key_count -= 1
        if key in self.non_primary_keys:
            self.non_primary_keys.remove(key)
        if key in self.table_data[0]:
            self.table_data[0].remove(key)
        elif key + "*" in self.table_data[0]:
            self.table_data[0].remove(key + "*")
        self.key_count -= 1
        self.remove_duplicate_rows()
        self.unique_counts = self._count_unique_instances_per_column()
        self.candidate_keys = self.calculate_candidate_keys()
        self.prime_attributes = self.calculate_prime_attributes()
        self.non_prime_attributes = self.calculate_non_prime_attributes()
    
    """Remove any duplicate rows."""
    def remove_duplicate_rows(self) -> None:
        self.rows = [list(t) for t in set(tuple(row) for row in self.rows)]
        self.table_data = [self.table_data[0]] + self.rows

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
        best_combination = None
        best_mml = float('inf')
        
        for comb in self.candidate_keys:
            # Calculates the MML value for the current combination
            mml_value = mml.I(1, self.key_count, [(self.key_count, len(comb))], [(len(self.rows), self.unique_counts)])
            # Break MML tiebreaks with the lowest number of attributes in primary key
            if mml_value < best_mml or (mml_value == best_mml and (best_combination is None or len(comb) < len(best_combination))):
                best_mml = mml_value
                best_combination = comb
        
        return best_combination, best_mml

    """
    Calculate all possible candidate keys for the table.
    """
    def calculate_candidate_keys(self) -> List[Tuple[str, ...]]:
        valid_combinations = self.get_valid_primary_key_combinations()
        candidate_keys = []
        for i in valid_combinations:
            for j in valid_combinations:
                # If there is another combination which is a proper subset of the current combination, then it cannot be a candidate key
                if set(j).issubset(set(i)) and set(i) != set(j):
                    break
            else:
                candidate_keys.append(i)
        return candidate_keys

    """
    Calculate all prime attributes for the table.
    """
    def calculate_prime_attributes(self) -> List[str]:
        prime_attribute_set = set()
        for tup in self.candidate_keys:
            for key in tup:
                prime_attribute_set.add(key)
        return list(prime_attribute_set)
    
    """
    Calculate all non-prime attributes for the table.
    """
    def calculate_non_prime_attributes(self) -> List[str]:
        prime_attribute_set = set()
        for tup in self.candidate_keys:
            for key in tup:
                prime_attribute_set.add(key)
        # Symmetric difference of all keys and prime attributes
        return list(set(self.keys) - prime_attribute_set)
    
    """Return a completely new table with the same table data but with no primary keys."""
    def return_stripped_table(self) -> Table:
        new_table_data = [self.keys] + self.rows
        return Table(new_table_data)
        
    """Display the table."""
    def display_table(self) -> None:
        for row in self.table_data:
            print('\t'.join(map(str, row)))
        
    """Print out all class variables of self."""
    def debug(self) -> None:
        print(f"Table Data: {self.table_data}")
        print(f"Keys: {self.keys}")
        print(f"Key Count: {self.key_count}")
        print(f"Primary Keys: {self.primary_keys}")
        print(f"Non-Primary Keys: {self.non_primary_keys}")
        print(f"Primary Key Count: {self.primary_key_count}")
        print(f"Rows: {self.rows}")
        print(f"Unique Counts: {self.unique_counts}")
        print(f"Candidate Keys: {self.candidate_keys}")
        print(f"Prime Attributes: {self.prime_attributes}")
        print(f"Non-Prime Attributes: {self.non_prime_attributes}")
