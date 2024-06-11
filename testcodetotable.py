import codetotable

############################# TEST H #############################
# Example for 1NF from paper, returns 14.55 (DA)
print(codetotable.H(1, 10, [(10, 3)]))
# Example for 2NF from paper, returns 45.06 (DA)
print(codetotable.H(3, 10, [(6, 1), (2, 1), (4, 3)]))
# Example for 3NF from paper, returns 56.61 (DA)
print(codetotable.H(4, 10, [(2, 1), (4, 3), (5, 1), (2, 1)]))

############################# TEST A #############################
# Example for 1NF from paper, returns 203.03 (A)
print(codetotable.A([(11, [5, 5, 5, 5, 4, 4, 2, 2, 3, 3])]))
# Example for 2NF from paper, returns 154.85 (DA)
print(codetotable.A([(5, [5, 5, 5, 5, 2, 2]), (4, [4, 4]), (11, [5, 4, 3, 3])]))
# Example for 3NF from paper, returns 153.85 (DA)
print(codetotable.A([(5, [5, 5, 5, 5, 2]), (2, [2, 2]), (4, [4, 4]), (11, [5, 4, 3, 3])]))

############################# TEST I #############################
# Example for 1NF from paper, returns 217.58 (DA)
print(codetotable.I(1, 10, [(10, 3)], [(11, [5, 5, 5, 5, 4, 4, 2, 2, 3, 3])]))
# Example for 2NF from paper, returns 199.91 (DA)
print(codetotable.I(3, 10, [(6, 1), (2, 1), (4, 3)], [(5, [5, 5, 5, 5, 2, 2]), (4, [4, 4]), (11, [5, 4, 3, 3])]))
# Example for 3NF from paper, returns 210.46 (DA)
print(codetotable.I(4, 10, [(2, 1), (4, 3), (5, 1), (2, 1)], [(5, [5, 5, 5, 5, 2]), (2, [2, 2]), (4, [4, 4]), (11, [5, 4, 3, 3])]))

############################# TEST I_to_LaTeX #############################
# Example from paper
print(codetotable.convert_to_LaTeX(["1NF", "2NF", "3NF"], [[10.22, 203.03, 213.25], [36.45, 154.89, 191.34], [46.26, 153.84, 200.10]]))