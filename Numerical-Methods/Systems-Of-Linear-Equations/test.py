import unittest
from methods import *

# run: python -m unittest -v test.py

class TestDeterminant(unittest.TestCase):

    def test_Det_invalid_shape(self):
        A = np.array([[1, 2], [2, 3], [3, 4]])
        self.assertAlmostEqual(determinant(A), None)
    
    def test_Det_one_num(self):
        A = np.array([[5]])
        self.assertAlmostEqual(determinant(A), 5)
    
    def test_Det_2x2(self):
        A = np.array([[1, 5], [4, 2]])
        self.assertAlmostEqual(determinant(A), -18)

    def test_Det_3x3(self):
        A = np.array([[1, -2, 3], [0, 7, 4], [5, 3, -3]])
        self.assertAlmostEqual(determinant(A), -178)

    def test_Det_4x4(self):
        A = np.array([[0, 3, -1, 1], [1, 2, 0, 0], [0, 4, 3, 5], [2, -1, -4, -2]])
        self.assertAlmostEqual(determinant(A), -58)


class TestCramer(unittest.TestCase):

    def test_Cramer_invalid_shape(self):
        A = np.array([[1, 2], [2, 3], [3, 4]])
        b = np.array([1, 2, 3])
        self.assertEqual(Cramer(A, b), None)

    def test_Cramer_zero_det(self):
        A = np.array([[1, 1, -2], [2, -3, -1], [1, -4, 1]])
        b = np.array([2, 1, 3])
        self.assertEqual(Cramer(A, b), None)
    
    def test_Cramer_2x2(self):
        A = np.array([[1, -2], [3, -4]])
        b = np.array([1, 7])
        for v1, v2 in zip(Cramer(A, b), [5, 2]):
            self.assertAlmostEqual(v1, v2)

    def test_Cramer_3x3(self):
        A = np.array([[1, 2, -3], [3, 2, -4], [2, -1, 0]])
        b = np.array([1, 0, -1])
        for v1, v2 in zip(Cramer(A, b), [-2, -3, -3]):
            self.assertAlmostEqual(v1, v2)

    def test_Cramer_4x4(self):
        A = np.array([[1, 3, 5, 7], [3, 5, 7, 1], [5, 7, 1, 3], [7, 1, 3, 5]])
        b = np.array([12, 0, 4, 16])
        for v1, v2 in zip(Cramer(A, b), [1, -1, 0, 2]):
            self.assertAlmostEqual(v1, v2)

class TestGauss(unittest.TestCase):

    def test_Gauss_invalid_shape(self):
        A = np.array([[1, 2], [2, 3], [3, 4]])
        b = np.array([1, 2, 3])
        self.assertEqual(Gauss(A, b), None)
    
    def test_Gauss_2x2(self):
        A = np.array([[1, -2], [3, -4]])
        b = np.array([1, 7])
        for v1, v2 in zip(Gauss(A, b), [5, 2]):
            self.assertAlmostEqual(v1, v2)

    def test_Gauss_3x3(self):
        A = np.array([[1, 2, -3], [3, 2, -4], [2, -1, 0]])
        b = np.array([1, 0, -1])
        for v1, v2 in zip(Gauss(A, b), [-2, -3, -3]):
            self.assertAlmostEqual(v1, v2)

    def test_Gauss_4x4(self):
        A = np.array([[1, 3, 5, 7], [3, 5, 7, 1], [5, 7, 1, 3], [7, 1, 3, 5]])
        b = np.array([12, 0, 4, 16])
        for v1, v2 in zip(Gauss(A, b), [1, -1, 0, 2]):
            self.assertAlmostEqual(v1, v2)

    
class TestDiagonalDominance(unittest.TestCase):

    def test_Diagonal_Dominance_false(self):
        A = np.array([[2, 2, 10], [10, 1, 1], [2, 10, 1]])
        b = np.array([14, 12, 13])
        self.assertFalse(CheckDiagonalDominance(A))
    
    def test_Diagonal_Dominance_true(self):
        A = np.array([[10, 1, 1], [2, 10, 1], [2, 2, 10]])
        b = np.array([12, 13, 14])
        self.assertTrue(CheckDiagonalDominance(A))


class TestCheckWithEpsilon(unittest.TestCase):

    def test_CheckWithEpsilon_true(self):
        vec1 = np.array([1, 2, 3])
        vec2 = np.array([1, 2.005, 3])
        epsilon = 0.01
        self.assertTrue(CheckWithEpsilon(vec1, vec2, epsilon))

    def test_CheckWithEpsilon_false(self):
        vec1 = np.array([1, 2, 3])
        vec2 = np.array([1, 2.005, 3])
        epsilon = 0.000001
        self.assertFalse(CheckWithEpsilon(vec1, vec2, epsilon))

class TestSimpleIterations(unittest.TestCase):

    def test_SimpleIterations_invalid_shape(self):
        A = np.array([[1, 2], [2, 3], [3, 4]])
        b = np.array([1, 2, 3])
        self.assertEqual(SimpleIterations(A, b, 0.00000001, 100), None)

    def test_SimpleIterations_not_diagonal_dominance(self):
        A = np.array([[2, 2, 10], [10, 1, 1], [2, 10, 1]])
        b = np.array([14, 12, 13])
        self.assertEqual(SimpleIterations(A, b, 0.00000001, 100), None)

    def test_SimpleIterations(self):
        A = np.array([[10, 1, 1], [2, 10, 1], [2, 2, 10]])
        b = np.array([12, 13, 14])
        for v1, v2 in zip(SimpleIterations(A, b, 0.00000001, 100), [1, 1, 1]):
            self.assertAlmostEqual(v1, v2)

    def test_SimpleIterations(self):
        A = np.array([[7.6, 0.6, 2.4], [-2.7, 4.2, 1.2], [1.8, 2.5, 4.7]])
        b = np.array([3, 2, 4])
        for v1, v2 in zip(SimpleIterations(A, b, 0.001, 100), [0.188, 0.441, 0.544]):
            self.assertAlmostEqual(v1, v2, places=2)


class TestSeidel(unittest.TestCase):

    def test_Seidel_invalid_shape(self):
        A = np.array([[1, 2], [2, 3], [3, 4]])
        b = np.array([1, 2, 3])
        self.assertEqual(Seidel(A, b, 0.00000001, 100), None)

    def test_Seidel_not_diagonal_dominance(self):
        A = np.array([[2, 2, 10], [10, 1, 1], [2, 10, 1]])
        b = np.array([14, 12, 13])
        self.assertEqual(Seidel(A, b, 0.00000001, 100), None)

    def test_Seidel(self):
        A = np.array([[10, 1, 1], [2, 10, 1], [2, 2, 10]])
        b = np.array([12, 13, 14])
        for v1, v2 in zip(Seidel(A, b, 0.00000001, 100), [1, 1, 1]):
            self.assertAlmostEqual(v1, v2)

    def test_Seidel(self):
        A = np.array([[7.6, 0.6, 2.4], [-2.7, 4.2, 1.2], [1.8, 2.5, 4.7]])
        b = np.array([3, 2, 4])
        for v1, v2 in zip(Seidel(A, b, 0.001, 100), [0.188, 0.441, 0.544]):
            self.assertAlmostEqual(v1, v2, places=2)


class TestRelax(unittest.TestCase):

    def test_Relax_invalid_shape(self):
        A = np.array([[1, 2], [2, 3], [3, 4]])
        b = np.array([1, 2, 3])
        self.assertEqual(UpperRelaxations(A, b, 0.5, 0.0001, 100), None)

    def test_Relax_not_diagonal_dominance(self):
        A = np.array([[2, 2, 10], [10, 1, 1], [2, 10, 1]])
        b = np.array([14, 12, 13])
        self.assertEqual(UpperRelaxations(A, b, 0.5, 0.0001, 100), None)

    def test_Relax(self):
        A = np.array([[10, 1, 1], [2, 10, 1], [2, 2, 10]])
        b = np.array([12, 13, 14])
        for v1, v2 in zip(UpperRelaxations(A, b, 1.5, 0.0001, 100), [1, 1, 1]):
            self.assertAlmostEqual(v1, v2)

    def test_Relax(self):
        A = np.array([[7.6, 0.6, 2.4], [-2.7, 4.2, 1.2], [1.8, 2.5, 4.7]])
        b = np.array([3, 2, 4])
        for v1, v2 in zip(UpperRelaxations(A, b, 1.5, 0.0001, 100), [0.188, 0.441, 0.544]):
            self.assertAlmostEqual(v1, v2, places=2)


class TestGaussJordan(unittest.TestCase):

    def test_GaussJordan_invalid_shape(self):
        A = np.array([[1, 2], [2, 3], [3, 4]])
        b = np.array([1, 2, 3])
        self.assertEqual(GaussJordan(A, b), None)
    
    def test_GaussJordan_2x2(self):
        A = np.array([[1, -2], [3, -4]])
        b = np.array([1, 7])
        for v1, v2 in zip(GaussJordan(A, b), [5, 2]):
            self.assertAlmostEqual(v1, v2)

    def test_GaussJordan_3x3(self):
        A = np.array([[1, 2, -3], [3, 2, -4], [2, -1, 0]])
        b = np.array([1, 0, -1])
        for v1, v2 in zip(GaussJordan(A, b), [-2, -3, -3]):
            self.assertAlmostEqual(v1, v2)

    def test_GaussJordan_4x4(self):
        A = np.array([[1, 3, 5, 7], [3, 5, 7, 1], [5, 7, 1, 3], [7, 1, 3, 5]])
        b = np.array([12, 0, 4, 16])
        for v1, v2 in zip(GaussJordan(A, b), [1, -1, 0, 2]):
            self.assertAlmostEqual(v1, v2)
