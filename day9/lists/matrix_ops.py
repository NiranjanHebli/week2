# matrix_ops.py - Matrix operations using plain lists


# Matrix Operations - Implementing addition, transpose, and multiplication for matrices represented as lists of lists.
def matrix_add(A, B):
    """
    Return the element-wise sum of two matrices A and B.
    Raises ValueError if dimensions don't match.
    """
    if len(A) != len(B) or any(len(A[i]) != len(B[i]) for i in range(len(A))):
        raise ValueError(
            f"Dimension mismatch for addition: "
            f"({len(A)}x{len(A[0])}) vs ({len(B)}x{len(B[0])})"
        )

    return [[A[i][j] + B[i][j] for j in range(len(A[i]))] for i in range(len(A))]


# Transpose of a matrix using nested list comprehension and zip.
def matrix_transpose(matrix):
    """
    Return the transpose of a matrix using nested list comprehension.
    Rows become columns and columns become rows.
    """
    return [list(row) for row in zip(*matrix)]


# Matrix multiplication using dot product logic.
def matrix_multiply(A, B):
    """
    Return the matrix product A x B using dot product logic.
    Raises ValueError if inner dimensions don't match.
    """
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise ValueError(
            f"Dimension mismatch for multiplication: "
            f"({rows_A}x{cols_A}) x ({rows_B}x{cols_B}) - "
            f"columns of A ({cols_A}) must equal rows of B ({rows_B})"
        )

    return [
        [sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A
    ]


# Helpers


# Pretty-printing a matrix for better visualization in test outputs.
def _fmt(matrix):
    """Pretty-print a matrix, one row per line."""
    return " [" + ",\n ".join(str(row) for row in matrix) + "]"


# Test Cases
def _run_tests():
    print("Matrix Operations - Test Cases\n")

    # 2x2 matrices
    print("\n2x2 Matrices\n\n")
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    print(f"  A = \n{_fmt(a)}\n")
    print(f"  B = \n{_fmt(b)}\n")

    print(f"\nmatrix_add(A, B)       =\n\n{_fmt(matrix_add(a, b))}")
    assert matrix_add(a, b) == [[6, 8], [10, 12]]

    print(f"\nmatrix_transpose(A)    =\n\n{_fmt(matrix_transpose(a))}")
    assert matrix_transpose(a) == [[1, 3], [2, 4]]

    print(f"\nmatrix_multiply(A, B)  =\n\n{_fmt(matrix_multiply(a, b))}")
    assert matrix_multiply(a, b) == [[19, 22], [43, 50]]

    # 3x3 matrices
    print("\n3x3 Matrices\n\n")
    c = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    d = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    print(f"  C = \n{_fmt(c)}\n")
    print(f"  D = \n{_fmt(d)}\n")

    print(f"\nmatrix_add(C, D)       =\n\n{_fmt(matrix_add(c, d))}")
    assert matrix_add(c, d) == [[10, 10, 10], [10, 10, 10], [10, 10, 10]]

    print(f"\nmatrix_transpose(C)    =\n\n{_fmt(matrix_transpose(c))}")
    assert matrix_transpose(c) == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    print(f"\nmatrix_multiply(C, D)  =\n\n{_fmt(matrix_multiply(c, d))}")
    assert matrix_multiply(c, d) == [[30, 24, 18], [84, 69, 54], [138, 114, 90]]

    # Non-square: 2x3 x 3x2
    print("\nNon-square (2x3) x (3x2)")
    e = [[1, 2, 3], [4, 5, 6]]  # 2x3
    f = [[7, 8], [9, 10], [11, 12]]  # 3x2
    result = matrix_multiply(e, f)
    print(f"  E (2x3) = {e}")
    print(f"  F (3x2) = {f}")
    print(f"  E x F   = {result}")
    assert result == [[58, 64], [139, 154]]

    # Dimension mismatch handling
    print("\nDimension Mismatch Handling")
    try:
        matrix_add([[1, 2]], [[1, 2, 3]])
    except ValueError as e:
        print(f"  matrix_add mismatch      - {e}")

    try:
        matrix_multiply([[1, 2]], [[1, 2]])
    except ValueError as e:
        print(f"  matrix_multiply mismatch - {e}")

    print("\nAll assertions passed.")


if __name__ == "__main__":
    _run_tests()
