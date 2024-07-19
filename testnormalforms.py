import normalforms
from table import Table
from typing import List, Tuple, Any

# Create sample tables
print("\n ------- 0NF Table(s) -------\n")
table_data = [
    ["EMPLOYEE_ID", "NAME", "JOB_CODE", "JOB", "STATE_CODE", "HOME_STATE"],
    [1, "Alice", 1, "Chef", 26, "Michigan"],
    [1, "Alice", 2, "Waiter", 26, "Michigan"],
    [2, "Charlie", 2, "Waiter", 56, "Wyoming"],
    [2, "Charlie", 3, "Bartender", 56, "Wyoming"],
    [3, "Alice", 1, "Chef", 56, "Wyoming"]
]
table_data2 = [
    ["studentName", "age", "GPA", "studentNo"],
    ["Maverick", 18, "2.5", 10393],
    ["Ash", 17, "3.2", 20392],
    ["Bobby", 19, "2.9", 12345],
    ["Alex", 18, "4.2", 29392],
    ["Alex", 18, "4.2", 19999]
]

table1 = Table(table_data)
table1.display_table()
print("\n")
table2 = Table(table_data2)
table2.display_table()

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
best_1NF_tables = normalforms.create_1NF_tables([table1, table2])
print("\n ------- Best 1NF Table(s) -------")
for t in best_1NF_tables:
    print("\nMML Value of Table: " + str(normalforms.calculate_mml([t])))
    t.display_table()
print("\nMML Value of All Table(s): " + str(normalforms.calculate_mml(best_1NF_tables)))
# Testing possible_partial_dependency function
# table2 = best_1NF_tables[1]
# print(table2.primary_keys)
# print(normalforms.possible_partial_dependency(table2, ("studentName", "age"), ("GPA", "studentNo"))) # Expected False
# print(normalforms.possible_partial_dependency(table2, ["studentName"], ["GPA"])) # Expected True
# print(normalforms.possible_partial_dependency(table2, ["studentName"], ["GPA", "studentNo"])) # Expected False
# print(normalforms.possible_partial_dependency(table2, ["studentName", "age"], ["GPA"])) # Expected True

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

# --- If you want to debug all found 2NF combinations, uncomment this and and uncomment return all table list line in the 2NF function ---
# debugging_best_2NF_tables = normalforms.create_2NF_tables(best_1NF_tables)
# print(debugging_best_2NF_tables)
# for table_list in debugging_best_2NF_tables:
#     for table_comb in table_list:
#         print("------------------------")
#         print(normalforms.calculate_mml(table_comb))
#         for table in table_comb:
#             table.display_table()