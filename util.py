from typing import List

def remove_asterisks(strings: List[str]) -> List[str]:
    return [s.rstrip('*') for s in strings]