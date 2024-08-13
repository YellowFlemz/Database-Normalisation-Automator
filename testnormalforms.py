import normalforms
from table import Table
from typing import List, Tuple, Any
import util

# Create sample tables
table_data1 = [
    ["EMPLOYEE_ID", "NAME", "JOB_CODE", "JOB", "STATE_CODE", "HOME_STATE"],
    [1, "Alice", 1, "Chef", 26, "Michigan"],
    [1, "Alice", 2, "Waiter", 26, "Michigan"],
    [2, "Charlie", 2, "Waiter", 56, "Wyoming"],
    [2, "Charlie", 3, "Bartender", 56, "Wyoming"],
    [3, "Alice", 1, "Chef", 56, "Wyoming"],
    [4, "Bob", 1, "Chef", 26, "Michigan"]
]
table_data2 = [
    ["studentName", "age", "GPA", "studentNo"],
    ["Maverick", 18, 2.5, 10393],
    ["Ash", 19, 3.3, 20392],
    ["Bobby", 19, 2.9, 12345],
    ["Alex", 18, 4.2, 29392],
    ["Alex", 18, 4.2, 19999],
    ["Maverick", 19, 4.2, 19998],
    ["Maverick", 19, 3.3, 10000],
    ["Bobby", 20, 2.9, 19392]
]
table_data3 = [
    ["Locker_ID", "Reservation_Start_Date", "Reservation_End_Date", "Reservation_End_Day"],
    [221, "14-May-2019", "12-Jun-2019", "Wednesday"],
    [308, "07-Jun-2019", "12-Jun-2019", "Wednesday"],
    [507, "14-May-2019", "17-May-2019", "Friday"],
    [221, "18-Jun-2019", "20-Jun-2019", "Thursday"],
    [308, "18-Jun-2019", "20-Jun-2019", "Thursday"],
    [308, "21-Jun-2019", "27-Jun-2019", "Thursday"]
]
table_data4 = [
    ["Restaurant", "Pizza Variety", "Delivery Area"],
    ["Pizza Hut", "Pepperoni", "Glen Waverley"],
    ["Pizza Hut", "Pepperoni", "Box Hill"],
    ["Pizza Hut", "Pepperoni", "Wantirna"],
    ["Pizza Hut", "Hawaiian", "Glen Waverley"],
    ["Pizza Hut", "Hawaiian", "Box Hill"],
    ["Pizza Hut", "Hawaiian", "Wantirna"],
    ["Domino's", "Cheese", "Wantirna"],
    ["Domino's", "Hawaiian", "Wantirna"],
    ["Factory 47", "Pepperoni", "Glen Waverley"],
    ["Factory 47", "Pepperoni", "Box Hill"],
    ["Factory 47", "Cheese", "Glen Waverley"],
    ["Factory 47", "Cheese", "Box Hill"]
]

# -----------------------   Tables to test go below   -----------------------
input_tables = [table_data4]

print("\n ------- 0NF Table(s) -------\n")
testingtables = []
for t in input_tables:
    temp = Table(t)
    temp.display_table()
    #temp.debug()
    testingtables.append(temp)
    print("\n")

# valid_primary_key_combinations1 = table1.get_valid_primary_key_combinations()
# valid_primary_key_combinations2 = table2.get_valid_primary_key_combinations()

# print("All valid combinations of primary keys for table 1:")
# for comb in valid_primary_key_combinations1:
#     print(comb)
# print("Unique instances per column:", table1.unique_counts)
# best_combination, best_mml = table1.calculate_best_primary_keys()
# print(f"Best combination for primary key: {best_combination} with MML: {best_mml}")

# print("All valid combinations of primary keys for table 2:")
# for comb in valid_primary_key_combinations2:
#     print(comb)
# print("Unique instances per column:", table2.unique_counts)
# best_combination, best_mml = table2.calculate_best_primary_keys()
# print(f"Best combination for primary key: {best_combination} with MML: {best_mml}")

# Create and display the new 1NF table
best_1NF_tables = normalforms.create_1NF_tables(testingtables)
print("------- Best 1NF Table(s) -------")
for t in best_1NF_tables:
    print("\nMML Value of Table: " + str(normalforms.calculate_mml([t])))
    t.display_table()
print("\nMML Value of All Table(s): " + str(normalforms.calculate_mml(best_1NF_tables)))

# Testing possible_functional_dependency function
# table2 = best_1NF_tables[1]
# print(table2.primary_keys)
# print(normalforms.possible_functional_dependency(table2, ("studentName", "age"), ("GPA", "studentNo"))) # Expected False
# print(normalforms.possible_functional_dependency(table2, ["studentName"], ["GPA"])) # Expected True
# print(normalforms.possible_functional_dependency(table2, ["studentName"], ["GPA", "studentNo"])) # Expected False
# print(normalforms.possible_functional_dependency(table2, ["studentName", "age"], ["GPA"])) # Expected True

# Test removing key column
# table1 = best_1NF_tables[0]
# table1.display_table()
# table1.remove_key_column("NAME")
# table1.debug()

# Test split_table function
# table1 = best_1NF_tables[0]
# print("Splitting table 1")
# table1.display_table()
# table1.debug()
# split_tables = normalforms.split_table(table1, ["EMPLOYEE_ID"], ["NAME", "STATE_CODE", "HOME_STATE"])
# for t in split_tables:
#     t.display_table()

# Testing create_2NF_tables function
best_2NF_tables = normalforms.create_2NF_tables(best_1NF_tables)
print("\n ------- Best 2NF Table(s) -------")
for t in best_2NF_tables:
    print("\nMML Value of Table: " + str(normalforms.calculate_mml([t])))
    t.display_table()
print("\nMML Value of All Table(s): " + str(normalforms.calculate_mml(best_2NF_tables)))

# Testing create_3NF_tables function
best_3NF_tables = normalforms.create_3NF_tables(best_2NF_tables)
print("\n ------- Best 3NF Table(s) -------")
for t in best_3NF_tables:
    print("\nMML Value of Table: " + str(normalforms.calculate_mml([t])))
    t.display_table()
print("\nMML Value of All Table(s): " + str(normalforms.calculate_mml(best_3NF_tables)))

# Testing create_BCNF_tables function
best_BCNF_tables = normalforms.create_BCNF_tables(best_3NF_tables)
print("\n ------- Best BCNF Table(s) -------")
for t in best_BCNF_tables:
    print("\nMML Value of Table: " + str(normalforms.calculate_mml([t])))
    t.display_table()
print("\nMML Value of All Table(s): " + str(normalforms.calculate_mml(best_BCNF_tables)))

# Testing create_4NF_tables function
best_4NF_tables = normalforms.create_4NF_tables(best_BCNF_tables)
print("\n ------- Best 4NF Table(s) -------")
for t in best_4NF_tables:
    print("\nMML Value of Table: " + str(normalforms.calculate_mml([t])))
    t.display_table()
print("\nMML Value of All Table(s): " + str(normalforms.calculate_mml(best_4NF_tables)))

# Testing possible_multivalued_dependency function
# table4 = best_3NF_tables[0]
# print(table4.primary_keys)
# print(normalforms.possible_multivalued_dependency(table4, ["Restaurant"], ["Pizza Variety"])) # Expected True
# print(normalforms.possible_multivalued_dependency(table4, ["Restaurant"], ["Delivery Area"])) # Expected True
# print(normalforms.possible_multivalued_dependency(table4, ["Pizza Variety"], ["Delivery Area"])) # Expected True


# --- If you want to debug all found 2NF combinations, uncomment below and uncomment return all table list line in the 2NF function ---
# debugging_best_2NF_tables = normalforms.create_2NF_tables(best_1NF_tables)
# print(debugging_best_2NF_tables)
# for table_list in debugging_best_2NF_tables:
#     for table_comb in table_list:
#         print("------------------------")
#         print(normalforms.calculate_mml(table_comb))
#         for table in table_comb:
#             table.display_table()

# --- If you want to debug all found 3NF combinations, uncomment below and uncomment return all table list line in the 3NF function ---
# debugging_best_3NF_tables = normalforms.create_3NF_tables(best_2NF_tables)
# print(debugging_best_3NF_tables)
# for table_list in debugging_best_3NF_tables:
#     for table_comb in table_list:
#         print("------------------------")
#         print(normalforms.calculate_mml(table_comb))
#         for table in table_comb:
#             table.display_table()

# --- If you want to debug all found 4NF combinations, uncomment below and uncomment return all table list line in the 4NF function ---
# debugging_best_4NF_tables = normalforms.create_4NF_tables(best_BCNF_tables)
# print(debugging_best_4NF_tables)
# for table_list in debugging_best_4NF_tables:
#     for table_comb in table_list:
#         print("------------------------")
#         print(normalforms.calculate_mml(table_comb))
#         for table in table_comb:
#             table.display_table()

# t1 = [["EMPLOYEE_ID", "STATE_CODE*", "NAME*", "HOME_STATE"],
# [1, 26, "Alice", "Michigan"],
# [2, 56, "Charlie", "Wyoming"],
# [3, 56, "Alice", "Wyoming"],
# [4, 26, "Bob", "Michigan"]]

# t2 = [["EMPLOYEE_ID*", "STATE_CODE", "NAME", "HOME_STATE"],
# [1, 26, "Alice", "Michigan"],
# [2, 56, "Charlie", "Wyoming"],
# [3, 56, "Alice", "Wyoming"],
# [4, 26, "Bob", "Michigan"]]

# print(normalforms.calculate_mml([Table(t1)]))
# print(normalforms.calculate_mml([Table(t2)]))