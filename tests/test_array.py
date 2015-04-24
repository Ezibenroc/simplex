from simplex import Array, DenseMatrix, SparseLine, SparseMatrix
from fractions import Fraction as F

from unittest import TestCase

class DenseTests(TestCase):

    def testConstructor(self):
        a = DenseMatrix([[1, 2], [3, 4]])
        self.assertEqual(a, [[1, 2], [3, 4]])
        self.assertIsInstance(a, DenseMatrix)
        for l in a:
            self.assertIsInstance(l, DenseMatrix)

    def testOperators(self):
        a = DenseMatrix([[F(1), F(2)], [F(3), F(4)]])
        b = DenseMatrix([[F(1), F(0)], [F(0), F(1)]])
        self.assertEqual(a+b, DenseMatrix([[2, 2], [3, 5]]))
        self.assertEqual(a-b, DenseMatrix([[0, 2], [3, 3]]))
        self.assertEqual(a*3, DenseMatrix([[3, 6], [9, 12]]))
        self.assertEqual(3*a, DenseMatrix([[3, 6], [9, 12]]))
        self.assertEqual(a/3, DenseMatrix([[F(1, 3), F(2, 3)], [1, F(4, 3)]]))
        a += b
        self.assertEqual(a, DenseMatrix([[2, 2], [3, 5]]))
        a -= b
        self.assertEqual(a, DenseMatrix([[1, 2], [3, 4]]))
        a*=3
        self.assertEqual(a, DenseMatrix([[3, 6], [9, 12]]))
        a/=3
        self.assertEqual(a, DenseMatrix([[1, 2], [3, 4]]))

    def testAddRemoveColumn(self):
        a = DenseMatrix([[F(1), F(2)], [F(3), F(4)]])
        a.addColumn(F(42), 1)
        self.assertEqual(a, DenseMatrix([[1, 42, 2], [3, 42, 4]]))
        a.removeColumn(2)
        self.assertEqual(a, DenseMatrix([[1, 42], [3, 42]]))
        a.addColumn(4)
        self.assertEqual(a, DenseMatrix([[4, 1, 42], [4, 3, 42]]))
        a.removeColumn()
        self.assertEqual(a, DenseMatrix([[1, 42], [3, 42]]))

class SparseTests(TestCase):

    def testConstructor(self):
        a = SparseLine([1, 2, 3, 4])
        self.assertEqual(a, [1, 2, 3, 4])

    def testOperators(self):
        a = SparseLine([F(1), F(2), F(3), F(4)])
        b = SparseLine([F(1), F(0), F(0), F(1)])
        self.assertEqual(a+b, SparseLine([2, 2, 3, 5]))
        self.assertEqual(a-b, SparseLine([0, 2, 3, 3]))
        self.assertEqual(a*3, SparseLine([3, 6, 9, 12]))
        self.assertEqual(3*a, SparseLine([3, 6, 9, 12]))
        self.assertEqual(a/3, SparseLine([F(1, 3), F(2, 3), 1, F(4, 3)]))
        a += b
        self.assertEqual(a, SparseLine([2, 2, 3, 5]))
        a -= b
        self.assertEqual(a, SparseLine([1, 2, 3, 4]))
        a*=3
        self.assertEqual(a, SparseLine([3, 6, 9, 12]))
        a/=3
        self.assertEqual(a, SparseLine([1, 2, 3, 4]))

    def testAddRemoveColumn(self):
        a = SparseLine([F(1), F(2), F(3), F(4)])
        a.addColumn(F(42), 1)
        self.assertEqual(a, SparseLine([1, 42, 2, 3, 4]))
        a.removeColumn(2)
        self.assertEqual(a, SparseLine([1, 42, 3, 4]))
        a.addColumn(4)
        self.assertEqual(a, SparseLine([4, 1, 42, 3, 4]))
        a.removeColumn()
        self.assertEqual(a, SparseLine([1, 42, 3, 4]))


    def testAddRemoveColumnMatrix(self):
        a = SparseMatrix([[F(1), F(2)], [F(3), F(4)]])
        a.addColumn(F(42), 1)
        self.assertEqual(a, SparseMatrix([[1, 42, 2], [3, 42, 4]]))
        a.removeColumn(2)
        self.assertEqual(a, SparseMatrix([[1, 42], [3, 42]]))
        a.addColumn(4)
        self.assertEqual(a, SparseMatrix([[4, 1, 42], [4, 3, 42]]))
        a.removeColumn()
        self.assertEqual(a, SparseMatrix([[1, 42], [3, 42]]))
