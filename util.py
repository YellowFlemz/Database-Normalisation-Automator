from typing import List, Tuple, Any
from itertools import combinations

# Remove asterisks from a list of strings
def remove_asterisks(strings: List[str]) -> List[str]:
    return [s.rstrip('*') for s in strings]

# Get all possible combinations of a list of data
def get_all_combinations(data: List[Any]) -> List[Tuple[Any]]:
    valid_combinations = []
    for r in range(1, len(data) + 1):
            valid_combinations.append(list(combinations(data, r)))
    return flattenlist(valid_combinations)

# Get all possible combinations of a list of data except for the case where all data is included
def get_all_combinations_except_all(data: List[Any]) -> List[Tuple[Any]]:
    valid_combinations = []
    for r in range(1, len(data)):
            valid_combinations.append(list(combinations(data, r)))
    return flattenlist(valid_combinations)

# Flatten a list of lists into one single list
def flattenlist(xss):
    return [x for xs in xss for x in xs]

# Transpose a list of lists (rows become columns and vice versa)
def transpose(matrix: List[List[Any]]) -> List[List[Any]]:
    return list(map(list, zip(*matrix)))
    