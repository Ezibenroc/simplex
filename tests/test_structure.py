from simplex import LinearProgram, EndOfAlgorithm, Unbounded

from unittest import TestCase
import numpy as np
from fractions import Fraction as F

testMatrix1 = np.matrix([
    [F(-3), F(2), F(-2), F(-1), F(0), F(0), F(0)],
    [F(4), F(-2), F(1), F(-1), F(1), F(0), F(-2)],
    [F(-1), F(1), F(-1), F(0), F(0), F(1), F(-10)],
])

testMatrix2 = np.matrix([
    [F(-5), F(-4), F(-3), F(0), F(0), F(0), F(0)],
    [F(2), F(3), F(1), F(1), F(0), F(0), F(5)],
    [F(4), F(1), F(2), F(0), F(1), F(0), F(11)],
    [F(3), F(4), F(2), F(0), F(0), F(1), F(8)],
])

class StructureTests(TestCase):

    def testConstructor(self):
        lp = LinearProgram(testMatrix1)
        self.assertEqual(lp.nbConstraints, 2)
        self.assertEqual(lp.nbVariables, 4)
        self.assertEqual(lp.basicVariables[1:], [4, 5])
        lp = LinearProgram(testMatrix2)
        self.assertEqual(lp.nbConstraints, 3)
        self.assertEqual(lp.nbVariables, 3)
        self.assertEqual(lp.basicVariables[1:], [3, 4, 5])

    def testChosePivot(self):
        lp = LinearProgram(testMatrix2)
        row, column = lp.chosePivot()
        self.assertEqual(column, 0)
        self.assertEqual(row, 1)
        for i in range(3):
            lp.tableaux[0, i] = F(1)
        with self.assertRaises(EndOfAlgorithm):
            row, column = lp.chosePivot()
        lp.tableaux[0, 0] = F(-1)
        for i in range(1, 4):
            lp.tableaux[i, 0] = F(-1)
        with self.assertRaises(Unbounded):
            row, column = lp.chosePivot()

    def testPerformPivot(self):
        lp = LinearProgram(testMatrix2)
        row, column = lp.chosePivot()
        self.assertEqual((row, column), (1, 0))
        lp.performPivot(row, column)
        expected = np.matrix([
            [F(0), F(7, 2), F(-1, 2), F(5, 2), F(0), F(0), F(25, 2)],
            [F(1), F(3, 2), F(1, 2), F(1, 2), F(0), F(0), F(5, 2)],
            [F(0), F(-5), F(0), F(-2), F(1), F(0), F(1)],
            [F(0), F(-1, 2), F(1, 2), F(-3, 2), F(0), F(1), F(1, 2)],
        ])
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], expected[i], "(row %d)" % i)
        self.assertEqual(lp.basicVariables[1:], [0, 4, 5])
        row, column = lp.chosePivot()
        self.assertEqual((row, column), (3, 2))
        lp.performPivot(row, column)
        expected = np.matrix([
            [F(0), F(3), F(0), F(1), F(0), F(1), F(13)],
            [F(1), F(2), F(0), F(2), F(0), F(-1), F(2)],
            [F(0), F(-5), F(0), F(-2), F(1), F(0), F(1)],
            [F(0), F(-1), F(1), F(-3), F(0), F(2), F(1)],
        ])
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], expected[i], "(row %d)" % i)
        self.assertEqual(lp.basicVariables[1:], [0, 4, 2])

    def testSimplex(self):
        lp = LinearProgram(testMatrix2)
        obj = lp.runSimplex()
        self.assertEqual(obj, 13)
        expected = np.matrix([
            [F(0), F(3), F(0), F(1), F(0), F(1), F(13)],
            [F(1), F(2), F(0), F(2), F(0), F(-1), F(2)],
            [F(0), F(-5), F(0), F(-2), F(1), F(0), F(1)],
            [F(0), F(-1), F(1), F(-3), F(0), F(2), F(1)],
        ])
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], expected[i], "(row %d)" % i)
        self.assertEqual(lp.basicVariables[1:], [0, 4, 2])
