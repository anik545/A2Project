import copy
import time
import fractions


class MatrixError(Exception):
    """ An exception class for Matrix """
    pass


class Matrix(object):
    def __init__(self, rows):
        self.y = len(rows)
        self.x = len(rows[0])
        for row in rows:
            if len(row) != self.x:
                raise MatrixError
        else:
            self.rows = [list(row) for row in rows]

    def __add__(self, other):
        if type(other) != Matrix:
            raise TypeError
        elif self.get_dimensions() != other.get_dimensions():
            raise MatrixError
        else:
            result = []
            for y in range(self.y):
                result.append([])
                for x in range(self.x):
                    result[y].append(self.rows[y][x] + other.rows[y][x])
            return Matrix(result)

    def __sub__(self, other):
        if type(other) != Matrix:
            raise TypeError
        elif self.get_dimensions() != other.get_dimensions():
            raise MatrixError
        else:
            result = []
            for y in range(self.y):
                result.append([])
                for x in range(self.x):
                    result[y].append(self.rows[y][x] - other.rows[y][x])
            return Matrix(result)

    def __mul__(self, other):
        if type(other) not in [Matrix, int, float]:
            raise TypeError
        elif type(other) == Matrix and self.get_dimensions()[1] != other.get_dimensions()[0]:
            raise MatrixError
        if type(other) == int or type(other) == float:
            result = [[0 for y in range(self.get_dimensions()[1])]
                      for x in range(self.get_dimensions()[0])]
            for y in range(self.y):
                for x in range(self.x):
                    result[y][x] = self.rows[y][x] * other
        else:
            result = [[0 for y in range(other.get_dimensions()[1])]
                      for x in range(self.get_dimensions()[0])]
            print(result)
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
        rows = self.rows
        return Matrix([[str(rows[y][x]) for x in range(self.x)] for y in range(self.y)])

    def get_dimensions(self):
        return (self.y, self.x)

    def get_rows(self):
        return self.rows

    def transpose(self):
        rows = self.rows
        return Matrix([[rows[x][y] for x in range(self.x)] for y in range(self.y)])

    def determinant(self):
        rows = self.rows
        if self.x != self.y:
            return None
        if self.x == 2:
            det = ((rows[0][0]) * (rows[1][1])) - (rows[0][1] * rows[1][0])
            return det
        else:
            top_row = rows[0]
            det = 0
            for x in range(len(top_row)):
                inner_mat = [[b for a, b in enumerate(
                    i) if a != x] for i in rows[1:]]
                inner_mat = Matrix(inner_mat)
                det += (-1)**x * top_row[x] * inner_mat.determinant()
            return det

    def display(self):
        for row in self.rows:
            for value in row:
                print(value, end=" ")
            print('\n', end='')

    def triangle(self):
        n = self.x
        mat = copy.deepcopy(self.rows)
        for i in range(n - 1):
            if mat[i][i] == 0:
                for j in range(i + 1, n, 1):
                    if mat[j][i] == 0:
                        continue
                    else:
                        mat[j], mat[i] = mat[i], mat[j]
            else:
                for k in range(i + 1, n):
                    ratio = fractions.Fraction(mat[k][i], mat[i][i])
                    for r in range(i, n, 1):
                        mat[k][r] -= ratio * mat[i][r]
                        # b[j] -= ratio*b[i] the column matrix Ax+By+Cz=(D)
        return Matrix(mat)

    def determinant2(self):
        if self.x != self.y:
            return None
        if self.x == 2:
            rows = self.rows
            det = ((rows[0][0]) * (rows[1][1])) - (rows[0][1] * rows[1][0])
            return det
        else:
            trimat = self.triangle().rows
            det = 1
            for x in range(len(trimat)):
                det *= trimat[x][x]
            return det

    def cofactors(self):
        rows = self.rows
        co_mat = copy.deepcopy(rows)
        for y in range(len(rows)):
            for x in range(len(rows[0])):
                inner_mat = [[b for a, b in enumerate(
                    j) if a != x] for i, j in enumerate(rows) if i != y]
                inner_mat = Matrix(inner_mat)
                co_mat[y][x] = (-1) ** (x + y) * inner_mat.determinant2()
        return Matrix(co_mat)

    def adjoint(self):
        return self.cofactors().transpose()

    def inverse(self):
        if self.x != self.y:
            raise MatrixError
        det = self.determinant()
        if det == 0:
            raise MatrixError
        c_t = self.adjoint().get_rows()
        for x in range(len(c_t)):
            for y in range(len(c_t[0])):
                c_t[x][y] = fractions.Fraction(c_t[x][y] / det).limit_denominator()
        return Matrix(c_t)

    @staticmethod
    def identity(size):
        id_mat = [[1 if x == y else 0 for y in range(
            size)] for x in range(size)]
        return Matrix(id_mat)

if __name__ == '__main__':
    a=Matrix([[5, 3, 4], [10, 7, 2], [10, 3, 7]])
    a.inverse().display()
