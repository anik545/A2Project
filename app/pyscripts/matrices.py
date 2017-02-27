import fractions


class MatrixError(Exception):
    """An exception class for Matrix."""

    pass


class Matrix(object):
    """Class for matrix operations."""

    def __init__(self, rows):
        """Return Matrix object given 2D list."""
        self.y = len(rows)
        self.x = len(rows[0])
        for row in rows:
            if len(row) != self.x:
                # All rows have to be the same row for a valid matrix
                raise MatrixError
        else:
            self.rows = [list(row) for row in rows]

    def __add__(self, other):
        """Override add operator to add matrix objects."""
        # Can only add matrices to matrices
        if type(other) != Matrix:
            raise TypeError
        # Both matrices have to be the same size to add
        elif self.get_dimensions() != other.get_dimensions():
            raise MatrixError
        else:
            # Create empty result list
            result = []
            for y in range(self.y):
                # Add empty row to result list
                result.append([])
                for x in range(self.x):
                    # Add values and add to row
                    result[y].append(self.rows[y][x] + other.rows[y][x])
            return Matrix(result)

    def __sub__(self, other):
        """Override subtract operator to subtract matrix objects."""
        # Can only subtract matrices from matrices
        if type(other) != Matrix:
            raise TypeError
        # Both matrices have to be the same size to subtract
        elif self.get_dimensions() != other.get_dimensions():
            raise MatrixError
        else:
            # Create empty result list
            result = []
            for y in range(self.y):
                # Add empty row to result list
                result.append([])
                for x in range(self.x):
                    # Subtract values and add to row
                    result[y].append(self.rows[y][x] - other.rows[y][x])
            return Matrix(result)

    def __mul__(self, other):
        """Override multiply operator to multiply matrix objects."""
        # Can only multiply a matrix by an integer, float or another matrix
        if type(other) not in [Matrix, int, float]:
            raise TypeError
        # Can only multiply by another matrix if width of one is height of other
        elif type(other) == Matrix and self.get_dimensions()[1] != other.get_dimensions()[0]:
            raise MatrixError
        # If multiplying by a int or float, multiply each element in matrix by the int or float
        if type(other) == int or type(other) == float:
            result = [[0 for y in range(self.get_dimensions()[1])]
                      for x in range(self.get_dimensions()[0])]
            for y in range(self.y):
                for x in range(self.x):
                    result[y][x] = self.rows[y][x] * other
        # If multiplying by another matrix, more complex
        else:
            # Empty result 2-d array with zeroes with correct dimensions
            result = [[0 for y in range(other.get_dimensions()[1])]
                      for x in range(self.get_dimensions()[0])]
            # Get data from 2 matrix objects
            a = self.rows
            b = other.rows
            for row in range(len(a)):
                for column in range(len(b[0])):
                    tot = 0
                    for x in range(len(a[0])):
                        tot += a[row][x] * b[x][column]
                    result[row][column] = tot
        return Matrix(result)

    def tostr(self):
        """Return Matrix with all elements converted to strings."""
        rows = self.rows
        return Matrix(
            [[str(rows[y][x]) for x in range(self.x)] for y in range(self.y)]
                )

    def get_dimensions(self):
        """Return dimensions of the matrix as a tuple."""
        return (self.y, self.x)

    def get_rows(self):
        """Get matrix data."""
        return self.rows

    def transpose(self):
        """Returned transposed matrix object."""
        rows = self.rows
        # List comprehension to flip matrix
        return Matrix(
            [[rows[x][y] for x in range(self.x)] for y in range(self.y)]
                )

    def determinant(self):
        """Return determinant of matrix as a float or int."""
        rows = self.rows
        if self.x != self.y:
            return MatrixError
        if self.x == 2:
            # For a 2x2 matrix [[a,b],[c,d]], the determinant is a*d-b*c
            det = ((rows[0][0]) * (rows[1][1])) - (rows[0][1] * rows[1][0])
            return det
        else:
            # For larger matrices
            # Get the top row of the matrix
            top_row = rows[0]
            # Initialize det variable
            det = 0
            # Loop over each item in the top row
            for x in range(len(top_row)):
                # Find the inner matrix
                # (the matrix got when you delete the row and column the item is in)
                inner_mat = [[b for a, b in enumerate(
                    i) if a != x] for i in rows[1:]]
                inner_mat = Matrix(inner_mat)
                # Find the determinant of the inner matrix
                # Multiply by the value in the row
                # Add or subtract depending on where in the row it is
                det += (-1)**x * top_row[x] * inner_mat.determinant()
            return det

    def display(self):
        """Print Matrix."""
        for row in self.rows:
            for value in row:
                print(value, end=" ")
            print('\n', end='')

    def triangle(self):
        """Return Matrix in triangle form."""
        n = self.x
        rows = self.rows
        # Loop from 0 to width-1
        for i in range(n - 1):
            if rows[i][i] == 0:
                for j in range(i + 1, n):
                    if rows[j][i] == 0:
                        # If all elements in the column are 0, do not swap rows
                        continue
                    else:
                        # Swap rows numbered j and i
                        rows[j], rows[i] = rows[i], rows[j]
            else:
                for k in range(i + 1, n):
                    # Get ratio between item in row i and row k (under i)
                    ratio = fractions.Fraction(rows[k][i], rows[i][i])
                    for r in range(i, n, 1):
                        # Subtract this row from row above * the ratio
                        # Means there is a 0 in first column(s)
                        rows[k][r] -= ratio * rows[i][r]
        return Matrix(rows)

    def cofactors(self):
        """Return cofactor matrix object."""
        co_mat = self.rows
        for y in range(len(co_mat)):
            for x in range(len(co_mat[0])):
                inner_mat = [[b for a, b in enumerate(
                    j) if a != x] for i, j in enumerate(co_mat) if i != y]
                inner_mat = Matrix(inner_mat)
                co_mat[y][x] = (-1) ** (x + y) * inner_mat.determinant()
        return Matrix(co_mat)

    def adjoint(self):
        """Return adjoint of matrix."""
        return self.cofactors().transpose()

    def inverse(self):
        """Return inverse of matrix."""
        # Can only find inverse of a square matrix
        if self.x != self.y:
            raise MatrixError
        det = self.determinant()
        # Can only find inverse if determinant is not 0
        if det == 0:
            raise MatrixError
        # Find the transpose of the cofactor matrix (the adjoint)
        c_t = self.adjoint().get_rows()
        # Divide every item in c_t by the determinant
        for x in range(len(c_t)):
            for y in range(len(c_t[0])):
                c_t[x][y] = fractions.Fraction(c_t[x][y] / det).limit_denominator()
        return Matrix(c_t)
