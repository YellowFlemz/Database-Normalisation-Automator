from table import Table
from typing import List

def create_1NF_tables(tables: List[Table]):
    res = []
    for table in tables:
        best_combination, _ = table.calculate_mml_for_combinations()
        new_keys = [f"{col}*" if col in best_combination else col for col in table.keys]
        
        # Create new table data with the updated keys
        new_table_data = [new_keys] + table.rows
        
        # Return a new Table object with the updated data
        res.append(Table(new_table_data))
    return res
