import normalforms
from table import Table

# Create sample tables
table_data = [
    ["id", "name", "age", "city"],
    [1, "Alice", 30, "Melbourne"],
    [2, "Bob", 25, "Sydney"],
    [3, "Charlie", 35, "Hobart"],
    [4, "Charlie", 23, "Melbourne"],
    [5, "Alice", 30, "Hobart"]
]

table_data2 = [
    ["studentNo", "studentName", "age", "GPA"],
    [10393, "Maverick", 18, "2.5"],
    [20392, "Ash", 17, "3.2"],
    [12345, "Bobby", 19, "2.9"],
    [29392, "Alex", 19, "4.2"],
    [19999, "Alex", 18, "4.5"]
]

table1 = Table(table_data)
table1.display_table()
table2 = Table(table_data2)
table2.display_table()

valid_primary_key_combinations1 = table1.get_valid_primary_key_combinations()
valid_primary_key_combinations2 = table2.get_valid_primary_key_combinations()

print("All valid combinations of primary keys for table 1:")
for comb in valid_primary_key_combinations1:
    print(comb)
print("Unique instances per column:", table1.unique_counts)
best_combination, best_mml = table1.calculate_best_primary_keys()
print(f"Best combination for primary key: {best_combination} with MML: {best_mml}")

print("All valid combinations of primary keys for table 2:")
for comb in valid_primary_key_combinations2:
    print(comb)
print("Unique instances per column:", table2.unique_counts)
best_combination, best_mml = table2.calculate_best_primary_keys()
print(f"Best combination for primary key: {best_combination} with MML: {best_mml}")

# Create and display the new 1NF table
best_1NF_tables = normalforms.create_1NF_tables([table1, table2])
print("\nBest 1NF Table(s):")
for t in best_1NF_tables:
    t.display_table()
print(normalforms.calculate_mml([table1, table2]))