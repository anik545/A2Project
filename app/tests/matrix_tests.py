import unittest
from app.pyscripts.matrices import *


class TestMatrices(unittest.TestCase):

    def setUp(self):
        self.mat1 = Matrix([[1, 2, 3], [14, 5, 1], [7, 3, 1]])
        self.mat2 = Matrix([[2, 3, 2], [7, 3, 6], [5, 2, 4]])
        self.mat3 = Matrix([[5, 1], [3, 1], [7, 4]])
        self.mat4 = Matrix([[5, 1, 6], [2, 3, 1]])

    def test_addition(self):
        self.assertEqual((self.mat1 + self.mat2).get_rows(),
                         [[3, 5, 5],
                          [21, 8, 7],
                          [12, 5, 5]])

    def test_subtraction(self):
        self.assertEqual((self.mat1 - self.mat2).get_rows(),
                         [[-1, -1, 1],
                          [7, 2, -5],
                          [2, 1, -3]])

    def test_multiply(self):
        self.assertEqual((self.mat1 * self.mat2).get_rows(),
                         [[31, 15, 26],
                          [68, 59, 62],
                          [40, 32, 36]])
        self.assertEqual((self.mat3 * self.mat4).get_rows(),
                         [[27, 8, 31],
                          [17, 6, 19],
                          [43, 19, 46]])

    def test_get_dimensions(self):
        self.assertEqual(self.mat1.get_dimensions(), (3, 3))
        self.assertEqual(self.mat3.get_dimensions(), (3, 2))
        self.assertEqual(self.mat4.get_dimensions(), (2, 3))

    def test_transpose(self):
        self.assertEqual(self.mat1.transpose().get_rows(),
                         [[1, 14, 7],
                          [2, 5, 3],
                          [3, 1, 1]])

    def test_determinant(self):
        self.assertEqual(self.mat1.determinant(), 9)
        self.assertRaises(MatrixError, self.mat3.determinant)

    def test_triangle(self):
        self.assertEqual(self.mat2.triangle().tostr().get_rows(),
                         [['2', '3', '2'],
                          ['0', '-15/2', '-1'],
                          ['0', '0', '-4/15']])

    def test_inverse(self):
        mat5 = Matrix([[-1, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.assertEqual(self.mat2.inverse().tostr().get_rows(),
                         [['0', '-5/2', '25/4'],
                          ['1/2', '5/4', '5/2'],
                          ['-1/4', '5/2', '5']])
        self.assertRaises(MatrixError, self.mat3.inverse)
        self.assertRaises(MatrixError, mat5.inverse)

unittest.main()
