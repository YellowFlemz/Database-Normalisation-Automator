from __future__ import annotations
from itertools import combinations
from typing import List, Tuple, Any
from copy import deepcopy
import codetotable as mml
import util

class Table:
    """
    Represents a table/relation in a database.

    Attributes:
        table_data (List[List[Any]]): The data of the table.
        keys (List[str]): The column names of the table.
        key_count (int): The number of columns in the table.
        primary_keys (List[str]): The primary keys of the table.
        non_primary_keys (List[str]): The non-primary keys of the table.
        primary_key_count (int): The number of primary keys in the table.
        rows (List[List[Any]]): The rows of data in the table.
        unique_counts (List[int]): The number of unique instances for each column.
        candidate_keys (List[Tuple[str, ...]]): The candidate keys of the table.
        prime_attributes (List[str]): The prime attributes of the table.
        non_prime_attributes (List[str]): The non-prime attributes of the table.
    """

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

    def get_key_column(self, key: str) -> List[Any]:
        """
        Retrieves the values from a specific key column in the table.

        Args:
            key (str): The key column (by name) to retrieve values from.

        Returns:
            List[Any]: A list of values from the specified key column.
        """
        key_index = self.keys.index(key)
        return [row[key_index] for row in self.rows]

    def remove_key_column(self, key: str) -> None:
        """
        Removes a key column from the table.
        Note: Do not pass in primary keys with asterisks (e.g. "studentNo*" should be passed as "studentNo")

        Args:
            key (str): The key column to be removed.

        Returns:
            None
        """
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

    def remove_duplicate_rows(self) -> None:
        """
        Removes duplicate rows from the table.
        Note: The first row (header) is not considered for duplicate removal.

        Returns:
            None
        """
        self.rows = [list(t) for t in set(tuple(row) for row in self.rows)]
        self.table_data = [self.table_data[0]] + self.rows

    def _count_unique_instances_per_column(self) -> List[int]:
        """
        Counts the number of unique instances per column in the table.

        Returns:
            A list of integers representing the number of unique instances per column.
        """
        unique_counts = []
        for col_index in range(len(self.keys)):
            # set() removes duplicates
            unique_values = set(row[col_index] for row in self.rows)
            unique_counts.append(len(unique_values))
        return unique_counts

    def _is_unique_combination(self, combination: Tuple[int, ...]) -> bool:
        """
        Checks if a combination of column indices in a row is unique.

        Args:
            combination (Tuple[int, ...]): A tuple of column indices.

        Returns:
            bool: True if the combination is unique in the table, False otherwise.
        """
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

    def get_valid_primary_key_combinations(self) -> List[Tuple[str, ...]]:
        """
        Returns a list of valid primary key combinations for the table.

        This method generates all possible combinations of the table's keys 
        and checks if each combination is unique.
        Only the combinations that are unique are considered valid primary key combinations.

        Returns:
            A list of tuples, where each tuple represents a valid primary key combination.
        """
        num_columns = len(self.keys)
        valid_combinations = []
        for r in range(1, num_columns + 1):
            # combinatorics to get all combinations of r columns
            for comb in combinations(range(num_columns), r):
                if self._is_unique_combination(comb):
                    valid_combinations.append(tuple(self.keys[i] for i in comb))
        return valid_combinations

    def calculate_best_primary_keys(self) -> Tuple[Tuple[str, ...], float]:
        """
        Calculates the best combination of valid primary keys for the table using 
        the Minimum Message Length (MML) criterion. Returns the one with the
        shortest MML.

        Returns:
            A tuple containing the best combination of primary keys and the corresponding MML value.
        """
        best_combination = None
        best_mml = float('inf')

        for comb in self.candidate_keys:
            # Calculates the MML value for the current combination
            mml_value = mml.I(1, self.key_count, [(self.key_count, len(comb))], \
                [(len(self.rows), self.unique_counts)])
            # Break MML tiebreaks with the lowest number of attributes in primary key
            if mml_value < best_mml or (mml_value == best_mml and \
                (best_combination is None or len(comb) < len(best_combination))):
                best_mml = mml_value
                best_combination = comb

        return best_combination, best_mml

    def calculate_candidate_keys(self) -> List[Tuple[str, ...]]:
        """
        Calculates and returns all possible candidate keys for the table.

        Returns:
            A list of tuples representing the candidate keys for the table.
        """
        valid_combinations = self.get_valid_primary_key_combinations()
        candidate_keys = []
        for i in valid_combinations:
            for j in valid_combinations:
                # If there is a combination which is a proper subset of the current combination,
                # then it cannot be a candidate key
                if set(j).issubset(set(i)) and set(i) != set(j):
                    break
            else:
                candidate_keys.append(i)
        return candidate_keys

    def calculate_prime_attributes(self) -> List[str]:
        """
        Calculates and returns the prime attributes of the table.

        Returns:
            A list of strings representing the prime attributes of the table.
        """
        prime_attribute_set = set()
        for tup in self.candidate_keys:
            for key in tup:
                prime_attribute_set.add(key)
        return list(prime_attribute_set)

    def calculate_non_prime_attributes(self) -> List[str]:
        """
        Calculates and returns the non-prime attributes of the table.

        Returns:
            A list of strings representing the non-prime attributes of the table.
        """
        prime_attribute_set = set()
        for tup in self.candidate_keys:
            for key in tup:
                prime_attribute_set.add(key)
        # Symmetric difference of all keys and prime attributes
        return list(set(self.keys) - prime_attribute_set)

    def return_stripped_table(self) -> Table:
        """
        Returns a new Table object with the same table data but with no primary keys.
        """
        new_table_data = deepcopy([self.keys]) + deepcopy(self.rows)
        return Table(new_table_data)

    def display_table(self) -> None:
        """
        Display the table data in a tabular format.

        Prints the keys and each row of the table, with columns separated by tabs.

        Returns:
            None
        """
        for row in self.table_data:
            print('\t'.join(map(str, row)))

    def debug(self) -> None:
        """
        This method prints various attributes and data of the Table object for debugging purposes.
        It displays table data, keys, key count, primary keys, non-primary keys, primary key count,
        rows, unique counts, candidate keys, prime attributes, and non-prime attributes.
        """
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
