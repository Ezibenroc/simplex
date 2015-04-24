from simplex import Array, SparseLine, SparseMatrix
from fractions import Fraction as F

from unittest import TestCase

class ArrayTests(TestCase):

    def testConstructor(self):
        a = Array([[1, 2], [3, 4]])
        self.assertEqual(a, [[1, 2], [3, 4]])
        self.assertIsInstance(a, Array)
        for l in a:
            self.assertIsInstance(l, Array)

    def testOperators(self):
        a = Array([[F(1), F(2)], [F(3), F(4)]])
        b = Array([[F(1), F(0)], [F(0), F(1)]])
        self.assertEqual(a+b, Array([[2, 2], [3, 5]]))
        self.assertEqual(a-b, Array([[0, 2], [3, 3]]))
        self.assertEqual(a*3, Array([[3, 6], [9, 12]]))
        self.assertEqual(3*a, Array([[3, 6], [9, 12]]))
        self.assertEqual(a/3, Array([[F(1, 3), F(2, 3)], [1, F(4, 3)]]))
        a += b
        self.assertEqual(a, Array([[2, 2], [3, 5]]))
        a -= b
        self.assertEqual(a, Array([[1, 2], [3, 4]]))
        a*=3
        self.assertEqual(a, Array([[3, 6], [9, 12]]))
        a/=3
        self.assertEqual(a, Array([[1, 2], [3, 4]]))

    def testAddRemoveColumn(self):
        a = Array([[F(1), F(2)], [F(3), F(4)]])
        a.addColumn(F(42), 1)
        self.assertEqual(a, Array([[1, 42, 2], [3, 42, 4]]))
        a.removeColumn(2)
        self.assertEqual(a, Array([[1, 42], [3, 42]]))
        a.addColumn(4)
        self.assertEqual(a, Array([[4, 1, 42], [4, 3, 42]]))
        a.removeColumn()
        self.assertEqual(a, Array([[1, 42], [3, 42]]))

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
