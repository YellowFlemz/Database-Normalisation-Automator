from table import Table
from typing import List, Tuple, Any
import codetotable as mml
import util
import copy

'''
    This function will take in a list of tables and return the list of tables in the best 1NF form according to MML.
'''
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

'''
    This function will take in a list of tables and return the list of tables in the best 2NF form according to MML.
'''
def create_2NF_tables(tables: List[Table]) -> List[Table]:
    
    possible_tables = []
    '''
    This function will recursively split a table into two tables using all possible partial dependencies.
    If the table cannot be split anymore, the tables will be added to the possible_tables list.
    In essence this function will find all possible table combinations that can be created from the given table 
    while following 2NF rules.
    '''
    def recursive_split(mainTable: Table, otherTables: List[Table] = []):
        p_key_subsets = util.get_all_combinations_except_all(mainTable.primary_keys)
        n_key_subsets = util.get_all_combinations(mainTable.non_primary_keys)
        for p_key_subset in p_key_subsets:
            for n_key_subset in n_key_subsets:
                if possible_partial_dependency(mainTable, p_key_subset, n_key_subset):
                    a, b = split_table(mainTable, p_key_subset, n_key_subset)
                    recursive_split(a, otherTables + [b])
                    recursive_split(b, otherTables + [a])
        # This ensures that the appended combination is in 2NF
        if cannot_be_split_further(mainTable):
            for table in otherTables:
                if not cannot_be_split_further(table):
                    break
            else:
                possible_tables.append([mainTable] + otherTables)
    
    def cannot_be_split_further(table: Table) -> bool:
        p_key_subsets = util.get_all_combinations_except_all(table.primary_keys)
        n_key_subsets = util.get_all_combinations(table.non_primary_keys)
        for p_key_subset in p_key_subsets:
            for n_key_subset in n_key_subsets:
                if possible_partial_dependency(table, p_key_subset, n_key_subset):
                    return False
        return True

    # Stores all possible 2NF table combinations for each table in tables
    all_table_list = []
    for table in tables:
        possible_tables = []
        recursive_split(table)
        all_table_list.append(possible_tables)
    # Use below line to help debug
    # return all_table_list

    # For each table in tables, finds the best 2NF table combination according to MML. This uses the combinations we identified previously.
    best_2nf_tables = []
    for table_list in all_table_list:
        best_mml = float('inf')
        best_table_combination = []
        for table_combination in table_list:
            if calculate_mml(table_combination) < best_mml:
                best_mml = calculate_mml(table_combination)
                best_table_combination = table_combination
        best_2nf_tables.append(best_table_combination)

    return util.flattenlist(best_2nf_tables)

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
    tabledatacopy = copy.deepcopy(table.table_data)
    # First table is created by simply removing the non-primary key columns (after deepcopying the original table data)
    first_table = Table(tabledatacopy)
    for key in nkeys:
        first_table.remove_key_column(key)
    # Second table is created by retrieving the values of the primary and non-primary key columns, and creating a new table
    pkeylist = [[pkeys[i] + "*"] + table.get_key_column(pkeys[i]) for i in range(len(pkeys))]
    nkeylist = [[nkeys[i]] + table.get_key_column(nkeys[i]) for i in range(len(nkeys))]
    # Table transposition is needed to get the correct table structure
    second_table = Table(util.transpose(pkeylist + nkeylist))
    return (first_table, second_table)
