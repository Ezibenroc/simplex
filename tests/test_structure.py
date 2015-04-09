from simplex import LinearProgram, EndOfAlgorithm, Unbounded, Empty

from unittest import TestCase
import numpy as np
from fractions import Fraction as F

testMatrix1 = np.array([
    [F(3), F(-2), F(2), F(1), F(0), F(0), F(0)],
    [F(4), F(-2), F(1), F(-1), F(1), F(0), F(-2)],
    [F(-1), F(1), F(-1), F(0), F(0), F(1), F(-10)],
])

testMatrix2 = np.array([
    [F(-5), F(-4), F(-3), F(0), F(0), F(0), F(0)],
    [F(2), F(3), F(1), F(1), F(0), F(0), F(5)],
    [F(4), F(1), F(2), F(0), F(1), F(0), F(11)],
    [F(3), F(4), F(2), F(0), F(0), F(1), F(8)],
])

testMatrix2FirstPhase = np.array([
    [F(1), F(-5), F(-4), F(-3), F(0), F(0), F(0), F(0)],
    [F(-1), F(2), F(3), F(1), F(1), F(0), F(0), F(5)],
    [F(-1), F(4), F(1), F(2), F(0), F(1), F(0), F(11)],
    [F(-1), F(3), F(4), F(2), F(0), F(0), F(1), F(8)],
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
        row, column = lp.choosePivot()
        self.assertEqual(column, 0)
        self.assertEqual(row, 1)
        for i in range(3):
            lp.tableaux[0][i] = F(1)
        with self.assertRaises(EndOfAlgorithm):
            row, column = lp.choosePivot()
        lp.tableaux[0][0] = F(-1)
        for i in range(1, 4):
            lp.tableaux[i][0] = F(-1)
        with self.assertRaises(Unbounded):
            row, column = lp.choosePivot()

    def testPerformPivot(self):
        lp = LinearProgram(testMatrix2)
        row, column = lp.choosePivot()
        self.assertEqual((row, column), (1, 0))
        lp.performPivot(row, column)
        expected = np.array([
            [F(0), F(7, 2), F(-1, 2), F(5, 2), F(0), F(0), F(25, 2)],
            [F(1), F(3, 2), F(1, 2), F(1, 2), F(0), F(0), F(5, 2)],
            [F(0), F(-5), F(0), F(-2), F(1), F(0), F(1)],
            [F(0), F(-1, 2), F(1, 2), F(-3, 2), F(0), F(1), F(1, 2)],
        ])
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], expected[i], "(row %d)" % i)
        self.assertEqual(lp.basicVariables[1:], [0, 4, 5])
        row, column = lp.choosePivot()
        self.assertEqual((row, column), (3, 2))
        lp.performPivot(row, column)
        expected = np.array([
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
        expected = np.array([
            [F(0), F(3), F(0), F(1), F(0), F(1), F(13)],
            [F(1), F(2), F(0), F(2), F(0), F(-1), F(2)],
            [F(0), F(-5), F(0), F(-2), F(1), F(0), F(1)],
            [F(0), F(-1), F(1), F(-3), F(0), F(2), F(1)],
        ])
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], expected[i], "(row %d)" % i)
        self.assertEqual(lp.basicVariables[1:], [0, 4, 2])

    def testAddRemoveVariable(self):
        lp = LinearProgram(testMatrix2)
        lp.addVariable()
        self.assertEqual(lp.nbVariables, 4)
        expected = testMatrix2FirstPhase
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], expected[i], "(row %d)" % i)
        lp.removeVariable()
        self.assertEqual(lp.nbVariables, 3)
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], testMatrix2[i], "(row %d)" % i)

    def testSolve(self):
        lp = LinearProgram(testMatrix1)
        objective = list(lp.tableaux[0])
        lp.tableaux[0] = [0]*len(lp.tableaux[0])
        lp.addVariable()
        row = lp.firstPhaseLeavingVariable()
        self.assertEqual(row, 2)
        lp.performPivot(row, 0)
        expected = np.array([
            [F(0), F(-1), F(1), F(-1), F(0), F(0), F(1), F(-10)],
            [F(0), F(5), F(-3), F(2), F(-1), F(1), F(-1), F(8)],
            [F(1), F(1), F(-1), F(1), F(0), F(0), F(-1), F(10)],
        ])
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], expected[i], "(row %d)" % i)
        row, column = 1, 3
        lp.performPivot(row, column)
        expected = np.array([
            [F(0), F(3, 2), F(-1, 2), F(0), F(-1, 2), F(1, 2), F(1, 2), F(-6)],
            [F(0), F(5, 2), F(-3, 2), F(1), F(-1, 2), F(1, 2), F(-1, 2), F(4)],
            [F(1), F(-3, 2), F(1, 2), F(0), F(1, 2), F(-1, 2), F(-1, 2), F(6)],
        ])
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], expected[i], "(row %d)" % i)
        row, column = 2, 2
        lp.performPivot(row, column)
        expected = np.array([
            [F(1), F(0), F(0), F(0), F(0), F(0), F(0), F(0)],
            [F(3), F(-2), F(0), F(1), F(1), F(-1), F(-2), F(22)],
            [F(2), F(-3), F(1), F(0), F(1), F(-1), F(-1), F(12)],
        ])
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], expected[i], "(row %d)" % i)
        lp.removeVariable()
        lp.tableaux[0] = objective
        lp.updateObjective()
        expected = np.array([
            [F(1), F(0), F(0), F(1), F(0), F(2), F(-20)],
            [F(-2), F(0), F(1), F(1), F(-1), F(-2), F(22)],
            [F(-3), F(1), F(0), F(1), F(-1), F(-1), F(12)],
        ])
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.tableaux[i], expected[i], "(row %d)" % i)

    def testSolve(self):
        lp = LinearProgram(testMatrix1)
        self.assertEqual(lp.solve(), -20)
        lp = LinearProgram(testMatrix2)
        self.assertEqual(lp.solve(), 13)

    def testTrivialEmpty(self):
        """
            Maximize 0 st x_0 <= 3 AND x_0 >= 4
        """
        lp = LinearProgram(np.array([
            [F(0), F(0), F(0), F(0)],
            [F(1), F(1), F(0), F(3)],
            [F(-1), F(0), F(1), F(-4)]
        ]))
        with self.assertRaises(Empty):
            lp.solve()

    def testTrivialUnbounded(self):
        """
            Maximize x_0 st x_0 >= 4
        """
        lp = LinearProgram(np.array([
            [F(-1), F(0), F(0)],
            [F(-1), F(1),F(-4)]
        ]))
        with self.assertRaises(Unbounded):
            lp.solve()
