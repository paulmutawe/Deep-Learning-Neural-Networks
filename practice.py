def rowsum(matrix):
    """
    :param matrix (list): A list of lists where each inner list represents a row.
    :returns: (list) A list containing the sum of each row.
    """
    row_sum = []
        
    for row in matrix:
        row_sum.append(sum(row))

    return row_sum

print(rowsum([[1, 2, 3], [4, 5, 6], [7, 8, 9]])) # Should print [6, 15, 24]