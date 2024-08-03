from table import Table
from typing import List, Tuple, Any
import codetotable as mml
import util
import copy

'''
    This function will take in a list of tables and return the list of tables in the best 1NF form according to MML.
    Working definition of 1NF:
    - There must be a primary key.
    - There are no repeating groups. (Not implemented)
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
    Working definition of 2NF:
    - The table is in 1NF.
    - No non-prime attribute in the table is partially dependent on any candidate key.
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
                if possible_functional_dependency(mainTable, p_key_subset, n_key_subset):
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
                if possible_functional_dependency(table, p_key_subset, n_key_subset):
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
        # Guarantees 2NF even if its MML value is worse than 1NF
        # Checks to see if there have been any splitting of tables; if so, remove all unsplit tables
        if max(len(comb) for comb in possible_tables) > 1:
            for comb in possible_tables:
                possible_tables = [comb for comb in possible_tables if len(comb) > 1]
        all_table_list.append(possible_tables)
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
    Working definition of 3NF:
    - The table is in 2NF
    - No non-prime attribute in the table is transitively dependent on the primary key.
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
        nonprimary_key_subsets = util.get_all_combinations_except_all(mainTable.non_primary_keys)
        nonprime_key_subsets = util.get_all_combinations(mainTable.non_prime_attributes)
        for nonprimary_key_subset in nonprimary_key_subsets:
            for nonprime_key_subset in nonprime_key_subsets:
                # Skip the iteration if there are any common attributes in the two subsets
                if len(set(nonprimary_key_subset).intersection(set(nonprime_key_subset))) > 0:
                    continue
                if possible_functional_dependency(mainTable, nonprimary_key_subset, nonprime_key_subset):
                    a, b = split_table(mainTable, nonprimary_key_subset, nonprime_key_subset)
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
        nonprimary_key_subsets = util.get_all_combinations_except_all(table.non_primary_keys)
        nonprime_key_subsets = util.get_all_combinations(table.non_prime_attributes)
        for nonprimary_key_subset in nonprimary_key_subsets:
            for nonprime_key_subset in nonprime_key_subsets:
                # Skip the iteration if there are any common attributes in the two subsets
                if len(set(nonprimary_key_subset).intersection(set(nonprime_key_subset))) > 0:
                    continue
                if possible_functional_dependency(table, nonprimary_key_subset, nonprime_key_subset):
                    return False
        return True

    # Stores all possible 3NF table combinations for each table in tables
    all_table_list = []
    for table in tables:
        possible_tables = []
        recursive_split(table)
        # Guarantees 3NF even if its MML value is worse than 2NF
        # Checks to see if there have been any splitting of tables; if so, remove all unsplit tables
        if max(len(comb) for comb in possible_tables) > 1:
            for comb in possible_tables:
                possible_tables = [comb for comb in possible_tables if len(comb) > 1]
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

'''
    This function will take in a list of tables and return the list of tables in the best BCNF form according to MML.
    Working definition of BCNF:
    - For every non-trivial functional dependency X -> Y, X is a superkey. 
'''
def create_BCNF_tables(tables: List[Table]) -> List[Table]:
    possible_tables = []
    '''
    This function will essentially do the same as 3NF but also looks for functional dependencies
    with prime attributes.
    '''
    def recursive_split(mainTable: Table, otherTables: List[Table] = []):
        primary_key_subsets = util.get_all_combinations_except_all(mainTable.primary_keys)
        prime_key_subsets = util.get_all_combinations(mainTable.prime_attributes)
        for primary_key_subset in primary_key_subsets:
            for prime_key_subset in prime_key_subsets:
                # Skip the iteration if there are any common attributes in the two subsets
                if len(set(primary_key_subset).intersection(set(prime_key_subset))) > 0:
                    continue
                if possible_functional_dependency(mainTable, primary_key_subset, prime_key_subset):
                    a, b = split_table(mainTable, primary_key_subset, prime_key_subset)
                    recursive_split(a, otherTables + [b])
                    recursive_split(b, otherTables + [a])
        # This ensures that the appended combination is in BCNF
        if cannot_be_split_further(mainTable):
            for table in otherTables:
                if not cannot_be_split_further(table):
                    break
            else:
                possible_tables.append([mainTable] + otherTables)

    def cannot_be_split_further(table: Table) -> bool:
        primary_key_subsets = util.get_all_combinations_except_all(table.primary_keys)
        prime_key_subsets = util.get_all_combinations(table.prime_attributes)
        for primary_key_subset in primary_key_subsets:
            for prime_key_subset in prime_key_subsets:
                # Skip the iteration if there are any common attributes in the two subsets
                if len(set(primary_key_subset).intersection(set(prime_key_subset))) > 0:
                    continue
                if possible_functional_dependency(table, primary_key_subset, prime_key_subset):
                    return False
        return True

    # Stores all possible BCNF table combinations for each table in tables
    all_table_list = []
    for table in tables:
        possible_tables = []
        # Run recursive_split() on all candidate keys of the table
        candidate_tables = all_candidate_tables(table)
        for t in candidate_tables:
            recursive_split(t)
        # Guarantees BCNF even if its MML value is worse than 3NF
        # Checks to see if there have been any splitting of tables; if so, remove all unsplit tables
        if max(len(comb) for comb in possible_tables) > 1:
            for comb in possible_tables:
                possible_tables = [comb for comb in possible_tables if len(comb) > 1]
        all_table_list.append(possible_tables)
    # Use below line to help debug
    # return all_table_list

    # For each table in tables, finds the best BCNF table combination according to MML. This uses the combinations identified previously.
    best_bcnf_tables = []
    for table_list in all_table_list:
        best_mml = float('inf')
        best_table_combination = []
        for table_combination in table_list:
            if calculate_mml(table_combination) < best_mml:
                best_mml = calculate_mml(table_combination)
                best_table_combination = table_combination
        best_bcnf_tables.append(best_table_combination)

    return util.flattenlist(best_bcnf_tables)

'''
    This function will take in a list of tables and return the list of tables in the best 4NF form according to MML.
    Working definition of 4NF:
    - For all multivalued dependencies X -> Y, {X, Y} is a superkey.
    - A multivalued dependency is defined as follows:
        - The table must contain at least 3 columns.
        - For a single value of A in the dependency A -> B, multiple values of B exist.
        - For the table T(A, B, C), if A -> B, then B and C must be independent of each other.
'''
def create_4NF_tables(tables: List[Table]) -> List[Table]:
    '''
    This function will look for multivalued dependencies and split if their union is not a superkey.
    '''
    def recursive_split(mainTable: Table, otherTables: List[Table] = []):
        key_subsets = util.get_all_combinations_except_all(mainTable.keys)
        for key_subset1 in key_subsets:
            for key_subset2 in key_subsets:
                # Skip the iteration if there are any common attributes in the two subsets
                if len(set(key_subset1).intersection(set(key_subset2))) > 0:
                    continue
                # Skip the iteration if the union of the two subsets is a superkey
                unionset = set(key_subset1).union(set(key_subset2))
                is_superkey = False
                for candidate_key in mainTable.candidate_keys:
                    if set(candidate_key).issubset(unionset):
                        is_superkey = True
                if is_superkey:
                    continue
                # Split if an illegal multivalued dependency is found
                if possible_multivalued_dependency(mainTable, key_subset1, key_subset2):
                    # Uses a different split_table call than previous NFs
                    a, b = split_table_4NF(mainTable, key_subset1, key_subset2)
                    recursive_split(a, otherTables + [b])
                    recursive_split(b, otherTables + [a])
        # This ensures that the appended combination is in BCNF
        if cannot_be_split_further(mainTable):
            for table in otherTables:
                if not cannot_be_split_further(table):
                    break
            else:
                possible_tables.append([mainTable] + otherTables)

    def cannot_be_split_further(table: Table) -> bool:
        key_subsets = util.get_all_combinations_except_all(table.keys)
        for key_subset1 in key_subsets:
            for key_subset2 in key_subsets:
                # Skip the iteration if there are any common attributes in the two subsets
                if len(set(key_subset1).intersection(set(key_subset2))) > 0:
                    continue
                # Skip the iteration if the union of the two subsets is a superkey
                unionset = set(key_subset1).union(set(key_subset2))
                is_superkey = False
                for candidate_key in table.candidate_keys:
                    if set(candidate_key).issubset(unionset):
                        is_superkey = True
                if is_superkey:
                    continue
                # Return False if an illegal multivalued dependency is found
                if possible_multivalued_dependency(table, key_subset1, key_subset2):
                    return False
        return True

    # Stores all possible BCNF table combinations for each table in tables
    all_table_list = []
    for table in tables:
        possible_tables = []
        # Run recursive_split() on all candidate keys of the table
        candidate_tables = all_candidate_tables(table)
        for t in candidate_tables:
            recursive_split(t)
        # Guarantees 4NF even if its MML value is worse than BCNF
        # Checks to see if there have been any splitting of tables; if so, remove all unsplit tables
        if max(len(comb) for comb in possible_tables) > 1:
            for comb in possible_tables:
                possible_tables = [comb for comb in possible_tables if len(comb) > 1]
        all_table_list.append(possible_tables)
    # Use below line to help debug
    # return all_table_list

    # For each table in tables, finds the best 4NF table combination according to MML. This uses the combinations identified previously.
    best_4nf_tables = []
    for table_list in all_table_list:
        best_mml = float('inf')
        best_table_combination = []
        for table_combination in table_list:
            if calculate_mml(table_combination) < best_mml:
                best_mml = calculate_mml(table_combination)
                best_table_combination = table_combination
        best_4nf_tables.append(best_table_combination)

    return util.flattenlist(best_4nf_tables)

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
    and we call possible_functional_dependency(t, ["studentName"], ["GPA", "studentNo"]).
    This will return False because for the studentName entry Alex, there are two different GPA and studentNo pairs (4.2, 29392) and (4.2, 19999).
    However if we call possible_functional_dependency(t, ["studentName"], ["GPA"]), this will return True because for each studentName entry, the GPA is the same.
    '''
def possible_functional_dependency(table: Table, keyset1: List[Any]|Tuple[Any], keyset2: List[Any]|Tuple[Any]) -> bool:
    # Implementation idea:
    # If we take the length of the set of the first keyset and the combined keyset, and they are the same, 
    # then we can say that the second set values always match the first set values (i.e. the first set key values don't conflict with their second set key values).
    # In contrast, if the length of the combined keyset > first keyset, then we can say that at least one of the first set keys has conflicting second set keys.
    # This checks the following condition:
    #   - For ANY single value of A in the dependency A -> B, exactly one value of B exists.
    keylist1 = [table.get_key_column(keyset1[i]) for i in range(len(keyset1))]
    keylist2 = [table.get_key_column(keyset2[i]) for i in range(len(keyset2))]
    combinedlist = keylist1 + keylist2
    solezipset = set(zip(*keylist1))
    combinedzipset = set(zip(*combinedlist))
    return len(solezipset) == len(combinedzipset)

def possible_multivalued_dependency(table: Table, keyset1: List[Any]|Tuple[Any], keyset2: List[Any]|Tuple[Any]) -> bool:
    # This checks the following condition:
    #   - The table must contain at least 3 columns.
    if len(table.keys) < 3:
        return False
    # This checks the following condition:
    #   - For a single value of A in the dependency A -> B, multiple values of B exist.
    # This code is similar to possible_functional_dependency but with the opposite check condition.
    keylist1 = [table.get_key_column(keyset1[i]) for i in range(len(keyset1))]
    keylist2 = [table.get_key_column(keyset2[i]) for i in range(len(keyset2))]
    combinedlist = keylist1 + keylist2
    solezipset = set(zip(*keylist1))
    combinedzipset = set(zip(*combinedlist))
    if len(solezipset) == len(combinedzipset):
        return False
    # This checks the following condition:
    #   - For the table T(A, B, C), if A -> B, then B and C must be independent of each other.
    return True

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
    Note that this function assumes that calling possible_functional_dependency with the same arguments will return True. 
    If this is not the case, the resulting tables may contain anomalies.
'''
def split_table(table: Table, pkeys: List[Any]|Tuple[Any], nkeys: List[Any]|Tuple[Any]) -> Tuple[Table, Table]:
    tabledatacopy = copy.deepcopy(table.table_data)
    # First table is created by simply removing the non-primary key columns (after deepcopying the original table data)
    first_table = Table(tabledatacopy)
    for key in nkeys:
        first_table.remove_key_column(key)
    # Second table is created by retrieving the values of the primary and non-primary key columns, and creating a new table
    # The primary and non-primary keys will retain their primary and non-primary attributes
    pkeylist = [[pkeys[i] + "*"] + table.get_key_column(pkeys[i]) for i in range(len(pkeys))]
    nkeylist = [[nkeys[i]] + table.get_key_column(nkeys[i]) for i in range(len(nkeys))]
    # Table transposition is needed to get the correct table structure
    second_table = Table(util.transpose(pkeylist + nkeylist))
    return (first_table, second_table)

'''
Similar to split_table, but both keyset1 and keyset2 will beecome primary keys in the second table.
'''
def split_table_4NF(table: Table, keyset1: List[Any]|Tuple[Any], keyset2: List[Any]|Tuple[Any]) -> Tuple[Table, Table]:
    tabledatacopy = copy.deepcopy(table.table_data)
    # First table is created by simply removing keyset2 (after deepcopying the original table data)
    first_table = Table(tabledatacopy)
    for key in keyset2:
        first_table.remove_key_column(key)
    # Second table is created by retrieving the values of the keyset1 and keyset2 columns, and creating a new table
    # However unlike split_table, both keyset1 and keyset2 are primary keys
    keylist1 = [[keyset1[i] + "*"] + table.get_key_column(keyset1[i]) for i in range(len(keyset1))]
    keylist2 = [[keyset2[i] + "*"] + table.get_key_column(keyset2[i]) for i in range(len(keyset2))]
    # Table transposition is needed to get the correct table structure
    second_table = Table(util.transpose(keylist1 + keylist2))
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