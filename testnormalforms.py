import normalforms
from table import Table

# Tables to test
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

table_data5 = [
    ["Salesman", "Brand", "Product"],
    ["Jack", "United", "Vacuum"],
    ["Jack", "United", "Breadbox"],
    ["Mary", "Borchio", "Scissors"],
    ["Mary", "Borchio", "Vacuum"],
    ["Mary", "Borchio", "Breadbox"],
    ["Mary", "Borchio", "Umbrella"],
    ["Bob", "Borchio", "Vacuum"],
    ["Bob", "Borchio", "Telescope"],
    ["Bob", "United", "Vacuum"],
    ["Bob", "United", "Lamp"],
    ["Bob", "Roless", "Tie"]
]

table_data6 = [
    ["Subject", "Lecturer", "Semester"],
    ["Computer Science", "Rhys", 1],
    ["Computer Science", "Blake", 1],
    ["Computer Science", "Blake", 2],
    ["Math", "Blake", 1],
    ["Math", "Marcus", 2],
    ["English", "Ryan", 1]
]

table_data7 = [
    ["Student ID", "Name", "Address", "Course", "Grade"],
    ["101", "Alice", "1 Main Street", "Math", "A"],
    ["101", "Alice", "1 Main Street", "English", "B"],
    ["101", "Alice", "1 Main Street", "History", "A"],
    ["102", "Bob", "2 Bowen Crescent", "Math", "B"],
    ["102", "Bob", "2 Bowen Crescent", "Biology", "C"],
    ["103", "Charlie", "3 Pine Road", "English", "A"],
    ["103", "Charlie", "3 Pine Road", "History", "A"],
    ["104", "Charlie", "3 Pine Road", "English", "A"],
]

table_data8 = [
    ["Club", "Year", "Captain's Player ID", "Captain's DOB"],
    ["Waverley", 2003, 1, "09/09/1979"],
    ["Ravens", 2002, 3, "01/11/1973"],
    ["Drillers", 2003, 1, "09/09/1979"],
    ["Waverley", 2002, 5, "14/02/1972"],
    ["Ravens", 2003, 4, "02/07/1975"],
    ["Waverley", 2004, 6, "14/02/1972"],
    ["Ravens", 2004, 2, "01/11/1973"],
    ["Drillers", 2004, 5, "14/02/1972"],
    ["Drillers", 2005, 5, "14/02/1972"],
]

table_data9 = [
    ["Student ID","Course", "Professor"],
    [101, "Math", "Dr. Smith"],
    [101, "Math", "Dr. Mack"],
    [101, "English", "Dr. Mack"],
    [102, "Biology", "Dr. Green"],
    [102, "Math", "Dr. Smith"],
    [103, "History", "Dr. Adams"],
    [103, "Math", "Dr. Smith"],
    [103, "Math", "Dr. Mack"],
]

table_data10 = [
    ["Project ID", "Employee ID", "Role"],
    [1, 1, "Manager"],
    [1, 2, "Developer"],
    [1, 3, "Developer"],
    [2, 1, "Manager"],
    [2, 2, "Developer"],
    [2, 3, "Developer"],
    [3, 1, "Manager"],
    [3, 2, "Developer"],
    [3, 4, "Developer"],
]

# -----------------------   Tables to test go below   -----------------------
input_tables = [table_data10]

print("\n ------- 0NF Table(s) -------\n")
testingtables = []
for t in input_tables:
    temp = Table(t)
    temp.display_table()
    testingtables.append(temp)
    print("\n")

# Testing create_1NF_tables function
best_1NF_tables = normalforms.create_1NF_tables(testingtables)
print("------- Best 1NF Table(s) -------")
for t in best_1NF_tables:
    print("\nMML Value of Table: " + str(normalforms.calculate_mml([t])))
    t.display_table()
    #t.debug()
print("\nMML Value of All Table(s): " + str(normalforms.calculate_mml(best_1NF_tables)))

# # Testing create_2NF_tables function
best_2NF_tables = normalforms.create_2NF_tables(best_1NF_tables)
print("\n ------- Best 2NF Table(s) -------")
for t in best_2NF_tables:
    print("\nMML Value of Table: " + str(normalforms.calculate_mml([t])))
    t.display_table()
    #t.debug()
print("\nMML Value of All Table(s): " + str(normalforms.calculate_mml(best_2NF_tables)))

# # Testing create_3NF_tables function
best_3NF_tables = normalforms.create_3NF_tables(best_2NF_tables)
print("\n ------- Best 3NF Table(s) -------")
for t in best_3NF_tables:
    print("\nMML Value of Table: " + str(normalforms.calculate_mml([t])))
    t.display_table()
print("\nMML Value of All Table(s): " + str(normalforms.calculate_mml(best_3NF_tables)))

# # Testing create_BCNF_tables function
best_BCNF_tables = normalforms.create_BCNF_tables(best_3NF_tables)
print("\n ------- Best BCNF Table(s) -------")
for t in best_BCNF_tables:
    print("\nMML Value of Table: " + str(normalforms.calculate_mml([t])))
    t.display_table()
print("\nMML Value of All Table(s): " + str(normalforms.calculate_mml(best_BCNF_tables)))

# # Testing create_4NF_tables function
best_4NF_tables = normalforms.create_4NF_tables(best_BCNF_tables)
print("\n ------- Best 4NF Table(s) -------")
for t in best_4NF_tables:
    print("\nMessage Length of Table and Data: " + str(normalforms.calculate_mml([t])))
    t.display_table()
print("\nMessage Length of All Table(s) and Data: " + str(normalforms.calculate_mml(best_4NF_tables)))

# # Testing create_5NF_tables function
best_5NF_tables = normalforms.create_5NF_tables(best_4NF_tables)
print("\n ------- Best 5NF Table(s) -------")
for t in best_5NF_tables:
    print("\nMessage Length of Table and Data: " + str(normalforms.calculate_mml([t])))
    t.display_table()
print("\nMessage Length of All Table(s) and Data: " + str(normalforms.calculate_mml(best_5NF_tables)))

# --- If you want to debug all found 2NF combinations, uncomment below, comment above 2NF lines
# and uncomment return all table list line in the 2NF function ---

# debugging_best_2NF_tables = normalforms.create_2NF_tables(best_1NF_tables)
# print(debugging_best_2NF_tables)
# for table_list in debugging_best_2NF_tables:
#     for table_comb in table_list:
#         print("------------------------")
#         print(normalforms.calculate_mml(table_comb))
#         for table in table_comb:
#             table.display_table()

# --- If you want to debug all found 3NF combinations, uncomment below, comment above 3NF lines
# and uncomment return all table list line in the 3NF function ---

# debugging_best_3NF_tables = normalforms.create_3NF_tables(best_2NF_tables)
# print(debugging_best_3NF_tables)
# for table_list in debugging_best_3NF_tables:
#     for table_comb in table_list:
#         print("------------------------")
#         print(normalforms.calculate_mml(table_comb))
#         for table in table_comb:
#             table.display_table()

# --- If you want to debug all found 4NF combinations, uncomment below, comment above 4NF lines
# and uncomment return all table list line in the 4NF function ---

# debugging_best_4NF_tables = normalforms.create_4NF_tables(best_BCNF_tables)
# print(debugging_best_4NF_tables)
# for table_list in debugging_best_4NF_tables:
#     for table_comb in table_list:
#         print("------------------------")
#         print(normalforms.calculate_mml(table_comb))
#         for table in table_comb:
#             table.display_table()
