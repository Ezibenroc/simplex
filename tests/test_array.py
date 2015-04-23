from simplex import Array
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
        self.assertEqual(a/3, Array([[F(1, 3), F(2, 3)], [1, F(4, 3)]]))
        a += b
        self.assertEqual(a, Array([[2, 2], [3, 5]]))
        a -= b
        self.assertEqual(a, Array([[1, 2], [3, 4]]))
        a*=3
        self.assertEqual(a, Array([[3, 6], [9, 12]]))
        a/=3
        self.assertEqual(a, Array([[1, 2], [3, 4]]))
