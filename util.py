from typing import List, Tuple, Any

def remove_asterisks(strings: List[str]) -> List[str]:
    return [s.rstrip('*') for s in strings]
