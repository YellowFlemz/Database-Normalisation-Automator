from table import Table
from typing import List, Tuple, Any
import codetotable as mml
import util

def create_1NF_tables(tables: List[Table]) -> List[Table]:
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
    # The goal of this function is to take in a list of tables and return them in the best 2NF form according to MML
    # First, for each table, we need to see if there is any possible partial dependency between all sets of primary keys and non-primary keys
    for table in tables:
        # TODO: if table has one p key, there are no partial dependencies. Figure out how to skip that table later
        dependencies = []
        p_key_subsets = util.get_all_combinations(table.primary_keys)
        n_key_subsets = util.get_all_combinations(table.non_primary_keys)
        for p_key_subset in p_key_subsets:
            for n_key_subset in n_key_subsets:
                if possible_partial_dependency(table, p_key_subset, n_key_subset):
                    dependencies.append((p_key_subset, "-->", n_key_subset))
        print(dependencies)

# Function that takes as input a list of tables and returns the MML encoding value
def calculate_mml(tables: List[Table]) -> float:
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

'''
    This function will return true if for each primary keyset, their respective non-primary keyset are the same.
    e.g. assume a table like t = [
    ["studentName", "age", "GPA", "studentNo"],
    ["Maverick", 18, "2.5", 10393],
    ["Ash", 17, "3.2", 20392],
    ["Bobby", 19, "2.9", 12345],
    ["Alex", 18, "4.2", 29392],
    ["Alex", 18, "4.2", 19999]]
    and we call is_partial_dependency(t, ["studentName"], ["GPA", "studentNo"]).
    This will return False because for the studentName entry Alex, there are two different GPA and studentNo pairs (4.2, 29392) and (4.2, 19999).
    However for simply is_partial_dependency(t, ["studentName"], ["GPA"]), this will return True because for each studentName entry, the GPA is the same.
    '''
def possible_partial_dependency(table: Table, pkeys: List[Any]|Tuple[Any], nkeys: List[Any]|Tuple[Any]) -> bool:
    # Implementation idea:
    # If we take the length of the set of the primary keyset and the combined keyset, and they are the same, 
    # then we can say that the non-primary values always match their primary values (i.e. the primary key values don't conflict with their non-primary key values).
    # In contrast, if the length of the combined keyset > primary keyset, then we can say that at least one of the primary keys has conflicting non-primary keys.
    pkeylist = [table.get_key_column(pkeys[i]) for i in range(len(pkeys))]
    nkeylist = [table.get_key_column(nkeys[i]) for i in range(len(nkeys))]
    combinedlist = pkeylist + nkeylist
    pkeyset = set(zip(*pkeylist))
    combinedset = set(zip(*combinedlist))
    return len(pkeyset) == len(combinedset)

'''
    This function aims to effectively split a table into two, like would be done in 2NF.
    e.g. assume a table like t = [
    ["studentName", "age", "GPA", "studentNo"],
    ["Maverick", 18, "2.5", 10393],
    ["Ash", 17, "3.2", 20392],
    ["Bobby", 19, "2.9", 12345],
    ["Alex", 18, "4.2", 29392],
    ["Alex", 18, "4.2", 19999]]
    and we call split_table(t, ["studentName"], ["GPA"]).
    The function should return two tables such as t1 = [
    ["studentName", "age", "studentNo"],
    ["Maverick", 18, 10393],
    ["Ash", 17, 20392],
    ["Bobby", 19, 12345],
    ["Alex", 18, 29392],
    ["Alex", 18, 19999]]
    ] and t2 = [
    ["studentName", "GPA"],
    ["Maverick", "2.5"],
    ["Ash", "3.2"],
    ["Bobby", "2.9"],
    ["Alex", "4.2"],
    ["Alex", "4.2"]]
    Note that this function assumes that calling possible_partial_dependency with the same arguments will return True.
'''
def split_table(table: Table, pkeys: List[Any]|Tuple[Any], nkeys: List[Any]|Tuple[Any]) -> Tuple[Table, Table]:
    pass
