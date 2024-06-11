import math

# Function to calculate #H
# A represents number of total attributes, at represents number of attributes in the current table, pt represents number of primary attributes in the current table
# e.g. tabletotal = 1, A = 10, at = 10, pt = 3
# call H(1, 10, [(10, 3)])
def H(tabletotal: int, a: int, tables: list[tuple[int, int]]) -> float:
    # Tabletotal is added to total as representation for unary coding
    total = len(tables) * math.log2(a) + tabletotal
    for table in tables:
        at, pt = table[0], table[1]
        total += (math.log2(math.comb(a, at)) + math.log2(at) + math.log2(math.comb(at, pt)))
    return round(total, 2)

# Function to calculate #A
# The initial integer is the number of rows (not including col names), each number represents the number of unique values in the column
# e.g. A = 11 * (log2(5) + log2(5) + log2(5) + log2(5) + log2(4) + log2(4) + log2(2) + log2(2) + log2(3) + log2(3))
# call A([(11, [5, 5, 5, 5, 4, 4, 2, 2, 3, 3])]
def A(data: list[tuple[int, list]]) -> float:
    total = float(0)
    for column in data:
        total += (column[0] * sum(map(lambda x: math.log2(x), column[1])))
    return round(total, 2)

# Function to calculate #I
# This is the final MML encoding value calculated by adding the values from #H and #A
# e.g. I = H(1, 10, [(10, 3)]) + A([(11, [5, 5, 5, 5, 4, 4, 2, 2, 3, 3])])
# call I(1, 10, [(10, 3)], [(11, [5, 5, 5, 5, 4, 4, 2, 2, 3, 3)])
def I(tabletotal: int, a: int, tables: list[tuple[int, int]], data: list[tuple[int, list]]) -> float:
    return round(H(tabletotal, a, tables) + A(data), 2)

# Function to create LaTeX table syntax
# refer to testcodetotable.py for example usage
def convert_to_LaTeX(nfs: list[str], values: list[list[float]]) -> str:
    if len(values) % 3 != 0 or len(values) != len(nfs):
        return "Invalid inputs"

    tablestring = ""
    for i in range(len(nfs)):
            # Values are to 2 DP
            tablestring += f"{nfs[i]}        &  {'{:.2f}'.format(values[i][0])}     &   {'{:.2f}'.format(values[i][2])}  &   {'{:.2f}'.format(values[i][2])} \\\\\n"
        
    return "\\begin{table}[h]\n\\begin{center}\n{\n\\small\n\n\\begin{tabular}{|c |c |c| c|}\n\\hline\n  &  $\\#H$ (first part's length) & $\\#A$ (second part's length) & total message length\\\\\n\\hline\n" + tablestring + "\\hline\n\\end{tabular}\n}\n\\end{center}\n\\caption{Code length (bits) of model and data for different NFs}\n\\label{tab_NF_result}\n\\end{table}"
