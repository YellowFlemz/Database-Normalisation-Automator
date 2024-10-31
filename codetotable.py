import math

def ptmultiplier(a, p, v=4):
    """
    Calculates the ptmultiplier value based on the given parameters. Its purpose
    is to increase the probability weighting towards tables with fewer primary keys.

    Parameters:
    a (int): The total number of attributes.
    p (int): The total number of prime attributes.
    v (int, optional): A calculation multiplier. Defaults to 4.

    Returns:
    float: The calculated ptmultiplier value.

    Raises:
    ValueError: If the p value is invalid.

    """
    if p >= 1 and p < a:
        return (1 - 1/v) * (1 / (math.pow(v, p-1)))
    if p == a:
        return math.pow(1/v, a-1)
    else:
        raise ValueError("Error: Invalid p value")

def H(tabletotal: int, a: int, atpttuples: list[tuple[int, int]]) -> float:
    """
    Function to calculate #H.
    e.g. tabletotal = 1, A = 10, at = 10, pt = 3
    call H(1, 10, [(10, 3)])

    Args:
        tabletotal (int): The total number of tables.
        a (int): The number of attributes.
        atpttuples (list[tuple[int, int]]): A list of tuples representing the attribute and primary key counts.

    Returns:
        float: The value of #H.

    """
    # Tabletotal is added to total as representation for unary coding
    total = len(atpttuples) * math.log2(a) + tabletotal
    for atpttuple in atpttuples:
        at, pt = atpttuple[0], atpttuple[1]
        # Primary key probability weighting applied
        total += (math.log2(math.comb(a, at)) + math.log2(at) + math.log2(math.comb(at, pt))) + -math.log2(ptmultiplier(at, pt))
    # return round(total, 2)
    return total

def A(data: list[tuple[int, list]]) -> float:
    """
    Function to calculate #A.
    e.g. A = 11 * (log2(5) + log2(5) + log2(5) + log2(5) + log2(4) + log2(4) + log2(2) + log2(2) + log2(3) + log2(3))
    call A([(11, [5, 5, 5, 5, 4, 4, 2, 2, 3, 3])]

    Parameters:
    data (list[tuple[int, list]]): A list of tuples. See example above.

    Returns:
        float: The value of #A.

    """
    total = float(0)
    for column in data:
        total += (column[0] * sum(map(lambda x: math.log2(x), column[1])))
    return total

def I(tabletotal: int, a: int, atpttuples: list[tuple[int, int]], data: list[tuple[int, list]]) -> float:
    """
    Function to calculate #I.
    e.g. I = H(1, 10, [(10, 3)]) + A([(11, [5, 5, 5, 5, 4, 4, 2, 2, 3, 3])])
    call I(1, 10, [(10, 3)], [(11, [5, 5, 5, 5, 4, 4, 2, 2, 3, 3)])

    Args:
        tabletotal (int): The total number of tables.
        a (int): The total number of attributes across all tables.
        atpttuples (list[tuple[int, int]]): A list of tuples representing the 
        attribute and primary key counts for each table.
        data (list[tuple[int, list]]): A list of tuples. See example above.

    Returns:
        float: The value of #I.

    """
    return round(H(tabletotal, a, atpttuples) + A(data), 2)

def convert_to_LaTeX(nfs: list[str], values: list[list[float]]) -> str:
    """
    Converts the given list of normalized forms (nfs) and their corresponding values
    into a LaTeX table string.
    Refer to testcodetotable.py for example usage.

    Args:
        nfs (list[str]): List of normalized forms.
        values (list[list[float]]): List of lists containing the values for each normalized form.

    Returns:
        str: LaTeX table string.

    """
    if len(values) % 3 != 0 or len(values) != len(nfs):
        return "Invalid inputs"

    tablestring = ""
    for i in range(len(nfs)):
            # Values are to 2 DP
            tablestring += f"{nfs[i]}        &  {'{:.2f}'.format(values[i][0])}     &   {'{:.2f}'.format(values[i][2])}  &   {'{:.2f}'.format(values[i][2])} \\\\\n"

    return "\\begin{table}[h]\n\\begin{center}\n{\n\\small\n\n\\begin{tabular}{|c |c |c| c|}\n\\hline\n  &  $\\#H$ (first part's length) & $\\#A$ (second part's length) & total message length\\\\\n\\hline\n" + tablestring + "\\hline\n\\end{tabular}\n}\n\\end{center}\n\\caption{Code length (bits) of model and data for different NFs}\n\\label{tab_NF_result}\n\\end{table}"
