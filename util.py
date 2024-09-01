from typing import List, Tuple, Any
from itertools import combinations

def remove_asterisks(strings: List[str]) -> List[str]:
    """
    Removes trailing asterisks from each string in the given list.

    Args:
        strings (List[str]): A list of strings.

    Returns:
        List[str]: A new list of strings with trailing asterisks removed.
    """
    return [s.rstrip('*') for s in strings]

def get_all_combinations(data: List[Any]) -> List[Tuple[Any]]:
    """
    Generates all possible combinations of elements from the given data.

    Args:
        data (List[Any]): A list of elements.

    Returns:
        List[Tuple[Any]]: A list of tuples representing all possible combinations
        of elements from the given data.
    """
    valid_combinations = []
    for r in range(1, len(data) + 1):
        valid_combinations.append(list(combinations(data, r)))
    return flattenlist(valid_combinations)

def get_all_combinations_except_all(data: List[Any]) -> List[Tuple[Any]]:
    """
    Generates all possible combinations of the elements in the given data list,
    except for the combination that includes all elements.

    Args:
        data (List[Any]): The list of elements to generate combinations from.

    Returns:
        List[Tuple[Any]]: A list of tuples representing the valid combinations.
    """
    valid_combinations = []
    for r in range(1, len(data)):
        valid_combinations.append(list(combinations(data, r)))
    return flattenlist(valid_combinations)

def flattenlist(xss):
    """
    Flatten a list of lists into one single list.

    Parameters:
    xss (list): A list of lists to be flattened.

    Returns:
    list: A single flattened list.
    """
    return [x for xs in xss for x in xs]

def transpose(matrix: List[List[Any]]) -> List[List[Any]]:
    """
    Transpose a list of lists (rows become columns and vice versa).

    Parameters:
        matrix (List[List[Any]]): The matrix to be transposed.

    Returns:
        List[List[Any]]: The transposed matrix.
    """
    return list(map(list, zip(*matrix)))
    