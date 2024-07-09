from table import Table
from typing import List
import codetotable as mml

def create_1NF_tables(tables: List[Table]):
    res = []
    for table in tables:
        best_combination, _ = table.calculate_best_primary_keys()
        new_keys = [f"{col}*" if col in best_combination else col for col in table.keys]
        
        # Create new table data with the updated keys
        new_table_data = [new_keys] + table.rows
        
        # Return a new Table object with the updated data
        res.append(Table(new_table_data))
    return res

def create_2NF_tables(tables: List[Table]):
    # Rearrange tables into all possible 2NF structures
    pass

# Function that takes as input a list of tables and returns the MML encoding value
def calculate_mml(tables: List[Table]):
    # Calculate tabletotal
    tablecount = len(tables)
    # Holds atpttuples
    tuplelist = []
    # Holds data
    datalist = []
    # Holds all seen attributes in the table list
    attributeset = set()
    for table in tables:
        attributeset.update(table.keys)
        # Calculate at
        attributecount = len(table.keys)
        # Calculate pt
        primarykeycount = len(table.primary_keys)
        # Append to tuplelist
        tuplelist.append((attributecount, primarykeycount))
        # Append to datalist
        datalist.append((len(table.rows), table.unique_counts))
    # Calculate a
    attributecount = len(attributeset)
    # Call and return I() with respective arguments
    return mml.I(tablecount, attributecount, tuplelist, datalist)