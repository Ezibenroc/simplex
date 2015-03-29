from simplex import LinearProgram, EndOfAlgorithm, Unbounded

from unittest import TestCase
import numpy as np
from fractions import Fraction as F

testMatrix1 = np.matrix([
    [F(-3), F(2), F(-2), F(-4), F(0), F(0), F(0)],
    [F(4), F(-2), F(1), F(-1), F(1), F(0), F(-2)],
    [F(-1), F(1), F(-1), F(0), F(0), F(1), F(-10)],
])

class StructureTests(TestCase):

    def testConstructor(self):
        lp = LinearProgram(testMatrix1)
        self.assertEqual(lp.nbConstraints, 2)
        self.assertEqual(lp.nbVariables, 4)

    def testChosePivot(self):
        lp = LinearProgram(testMatrix1)
        row, column = lp.chosePivot()
        self.assertEqual(column, 1)
        self.assertEqual(row, 1)
        lp.tableaux[0, 1] = F(-1)
        with self.assertRaises(EndOfAlgorithm):
            row, column = lp.chosePivot()
        lp.tableaux[0, 1] = F(2)
        lp.tableaux[1, 1] = F(2)
        with self.assertRaises(Unbounded):
            row, column = lp.chosePivot()

    def testPerformPivot(self):
        lp = LinearProgram(testMatrix1)
        row, column = 1, 1
        lp.performPivot(row, column)
        expected = np.matrix([
            [F(1), F(0), F(-1), F(-5), F(1), F(0), F(-2)],
            [F(-2), F(1), F(-1, 2), F(1, 2), F(-1, 2), F(0), F(1)],
            [F(1), F(0), F(-1, 2), F(-1, 2), F(1, 2), F(1), F(-11)],
        ])
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], expected[i], "(row %d)" % i)
