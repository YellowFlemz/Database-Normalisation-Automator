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
        n_key_subsets = util.get_all_combinations(mainTable.non_prime_attributes)
        for p_key_subset in p_key_subsets:
            for n_key_subset in n_key_subsets:
                if possible_dependency(mainTable, p_key_subset, n_key_subset):
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
        n_key_subsets = util.get_all_combinations(table.non_prime_attributes)
        for p_key_subset in p_key_subsets:
            for n_key_subset in n_key_subsets:
                if possible_dependency(table, p_key_subset, n_key_subset):
                    return False
        return True

    # Stores all possible 2NF table combinations for each table in tables
    all_table_list = []
    for table in tables:
        possible_tables = []
        # Run recursive_split() on all candidate keys of the table
        candidate_tables = all_candidate_tables(table)
        for t in candidate_tables:
            recursive_split(t)
        all_table_list.append(possible_tables)
        # Guarantees 2NF even if its MML value is worse than 1NF
        if len(possible_tables) > len(candidate_tables):
            for comb in possible_tables:
                if len(comb) == 1:
                    possible_tables.remove(comb)
    # Use below line to help debug
    # return all_table_list

    # For each table in tables, finds the best 2NF table combination according to MML. This uses the combinations identified previously.
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

'''
    This function will take in a list of tables and return the list of tables in the best 3NF form according to MML.
'''
def create_3NF_tables(tables: List[Table]) -> List[Table]:
    possible_tables = []
    '''
    This function will recursively split a table into two tables using all possible transitive dependencies.
    If the table cannot be split anymore, the tables will be added to the possible_tables list.
    In essence this function will find all possible table combinations that can be created from the given table 
    while following 3NF rules.
    '''
    def recursive_split(mainTable: Table, otherTables: List[Table] = []):
        n_key_subsets = util.get_all_combinations_except_all(mainTable.non_primary_keys)
        for subset1 in n_key_subsets:
            for subset2 in n_key_subsets:
                # Skip checking for dependencies if the chosen keysets have any intersecting values (keys cannot exist in both sets)
                if len(set(subset1).intersection(set(subset2))) > 0:
                    continue
                if possible_dependency(mainTable, subset1, subset2):
                    a, b = split_table(mainTable, subset1, subset2)
                    recursive_split(a, otherTables + [b])
                    recursive_split(b, otherTables + [a])
        # This ensures that the appended combination is in 3NF
        if cannot_be_split_further(mainTable):
            for table in otherTables:
                if not cannot_be_split_further(table):
                    break
            else:
                possible_tables.append([mainTable] + otherTables)

    def cannot_be_split_further(table: Table) -> bool:
        n_key_subsets = util.get_all_combinations_except_all(table.non_primary_keys)
        for subset1 in n_key_subsets:
            for subset2 in n_key_subsets:
                if len(set(subset1).intersection(set(subset2))) > 0:
                    continue
                if possible_dependency(table, subset1, subset2):
                    return False    
        return True

    # Stores all possible 3NF table combinations for each table in tables
    all_table_list = []
    for table in tables:
        possible_tables = []
        recursive_split(table)
        all_table_list.append(possible_tables)
    # Use below line to help debug
    # return all_table_list

    # For each table in tables, finds the best 3NF table combination according to MML. This uses the combinations identified previously.
    best_3nf_tables = []
    for table_list in all_table_list:
        best_mml = float('inf')
        best_table_combination = []
        for table_combination in table_list:
            if calculate_mml(table_combination) < best_mml:
                best_mml = calculate_mml(table_combination)
                best_table_combination = table_combination
        best_3nf_tables.append(best_table_combination)

    return util.flattenlist(best_3nf_tables)

# Function that takes as input a list of tables and returns the MML encoding value
def calculate_mml(tables: List[Table]) -> float:
    if len(tables) == 0 or tables == [[]]:
        return None
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
    This function will return true if for each key value in the first keyset, their respective key value in the second keyset are always the same in the table.
    e.g. assume a table like t = [
    ["studentName", "age", "GPA", "studentNo"],
    ["Maverick", 18, "2.5", 10393],
    ["Ash", 17, "3.2", 20392],
    ["Bobby", 19, "2.9", 12345],
    ["Alex", 18, "4.2", 29392],
    ["Alex", 18, "4.2", 19999]]
    and we call possible_dependency(t, ["studentName"], ["GPA", "studentNo"]).
    This will return False because for the studentName entry Alex, there are two different GPA and studentNo pairs (4.2, 29392) and (4.2, 19999).
    However if we call possible_dependency(t, ["studentName"], ["GPA"]), this will return True because for each studentName entry, the GPA is the same.
    '''
def possible_dependency(table: Table, keyset1: List[Any]|Tuple[Any], keyset2: List[Any]|Tuple[Any]) -> bool:
    # Implementation idea:
    # If we take the length of the set of the first keyset and the combined keyset, and they are the same, 
    # then we can say that the second set values always match the first set values (i.e. the first set key values don't conflict with their second set key values).
    # In contrast, if the length of the combined keyset > first keyset, then we can say that at least one of the first set keys has conflicting second set keys.
    keylist1 = [table.get_key_column(keyset1[i]) for i in range(len(keyset1))]
    keylist2 = [table.get_key_column(keyset2[i]) for i in range(len(keyset2))]
    combinedlist = keylist1 + keylist2
    solezipset = set(zip(*keylist1))
    combinedzipset = set(zip(*combinedlist))
    return len(solezipset) == len(combinedzipset)

'''
    This function aims to effectively split a table into two, like would be done in 2NF/3NF.
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
    and t2 = [
    ["studentName", "GPA"],
    ["Maverick", "2.5"],
    ["Ash", "3.2"],
    ["Bobby", "2.9"],
    ["Alex", "4.2"],
    ["Alex", "4.2"]
    ]
    Note that this function assumes that calling possible_dependency with the same arguments will return True. 
    If this is not the case, the resulting tables may contain anomalies.
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

'''
Given a table, returns a List of tables using all possible candidate keys of the table.
'''
def all_candidate_tables(table: Table) -> List[Table]:
    res = []
    for tup in table.candidate_keys:
        keys = copy.deepcopy(table.keys)
        for i in range(len(keys)):
            if keys[i] in tup:
                keys[i] = keys[i] + "*"
        res.append(Table([keys] + table.rows))
    return res