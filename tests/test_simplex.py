from simplex import Simplex, EndOfAlgorithm, Unbounded, Empty, Array

from unittest import TestCase
from fractions import Fraction as F

testMatrix1 = [
    [F(3), F(-2), F(2), F(1), F(0), F(0), F(0)],
    [F(4), F(-2), F(1), F(-1), F(1), F(0), F(-2)],
    [F(-1), F(1), F(-1), F(0), F(0), F(1), F(-10)],
]

testMatrix2 = [
    [F(-5), F(-4), F(-3), F(0), F(0), F(0), F(0)],
    [F(2), F(3), F(1), F(1), F(0), F(0), F(5)],
    [F(4), F(1), F(2), F(0), F(1), F(0), F(11)],
    [F(3), F(4), F(2), F(0), F(0), F(1), F(8)],
]

testMatrix2FirstPhase = [
    [F(1), F(-5), F(-4), F(-3), F(0), F(0), F(0), F(0)],
    [F(-1), F(2), F(3), F(1), F(1), F(0), F(0), F(5)],
    [F(-1), F(4), F(1), F(2), F(0), F(1), F(0), F(11)],
    [F(-1), F(3), F(4), F(2), F(0), F(0), F(1), F(8)],
]

class StructureTests(TestCase):

    def testConstructor(self):
        s = Simplex(testMatrix1)
        self.assertEqual(s.nbConstraints, 2)
        self.assertEqual(s.nbVariables, 4)
        self.assertEqual(s.basicVariables[1:], [4, 5])
        for i in range(len(testMatrix1)):
            self.assertEqual(s.tableaux[i], testMatrix1[i])
        s = Simplex(testMatrix2)
        self.assertEqual(s.nbConstraints, 3)
        self.assertEqual(s.nbVariables, 3)
        self.assertEqual(s.basicVariables[1:], [3, 4, 5])
        for i in range(len(testMatrix2)):
            self.assertEqual(s.tableaux[i], testMatrix2[i])

    def testChosePivot(self):
        s = Simplex(testMatrix2)
        row, column = s.choosePivot()
        self.assertEqual(column, 0)
        self.assertEqual(row, 1)
        for i in range(3):
            s.tableaux[0][i] = F(1)
        with self.assertRaises(EndOfAlgorithm):
            row, column = s.choosePivot()
        s.tableaux[0][0] = F(-1)
        for i in range(1, 4):
            s.tableaux[i][0] = F(-1)
        with self.assertRaises(Unbounded):
            row, column = s.choosePivot()

    def testPerformPivot(self):
        s = Simplex(testMatrix2)
        row, column = s.choosePivot()
        self.assertEqual((row, column), (1, 0))
        s.performPivot(row, column)
        expected = Array([
            [F(0), F(7, 2), F(-1, 2), F(5, 2), F(0), F(0), F(25, 2)],
            [F(1), F(3, 2), F(1, 2), F(1, 2), F(0), F(0), F(5, 2)],
            [F(0), F(-5), F(0), F(-2), F(1), F(0), F(1)],
            [F(0), F(-1, 2), F(1, 2), F(-3, 2), F(0), F(1), F(1, 2)],
        ])
        for i in range(len(expected)):
            self.assertEqual(s.tableaux[i], expected[i], "(row %d)" % i)
        self.assertEqual(s.basicVariables[1:], [0, 4, 5])
        row, column = s.choosePivot()
        self.assertEqual((row, column), (3, 2))
        s.performPivot(row, column)
        expected = Array([
            [F(0), F(3), F(0), F(1), F(0), F(1), F(13)],
            [F(1), F(2), F(0), F(2), F(0), F(-1), F(2)],
            [F(0), F(-5), F(0), F(-2), F(1), F(0), F(1)],
            [F(0), F(-1), F(1), F(-3), F(0), F(2), F(1)],
        ])
        for i in range(len(expected)):
            self.assertEqual(s.tableaux[i], expected[i], "(row %d)" % i)
        self.assertEqual(s.basicVariables[1:], [0, 4, 2])

    def testSimplex(self):
        s = Simplex(testMatrix2)
        obj = s.runSimplex()
        self.assertEqual(obj, 13)
        expected = Array([
            [F(0), F(3), F(0), F(1), F(0), F(1), F(13)],
            [F(1), F(2), F(0), F(2), F(0), F(-1), F(2)],
            [F(0), F(-5), F(0), F(-2), F(1), F(0), F(1)],
            [F(0), F(-1), F(1), F(-3), F(0), F(2), F(1)],
        ])
        for i in range(len(expected)):
            self.assertEqual(s.tableaux[i], expected[i], "(row %d)" % i)
        self.assertEqual(s.basicVariables[1:], [0, 4, 2])

    def testAddRemoveVariable(self):
        s = Simplex(testMatrix2)
        s.addVariable()
        self.assertEqual(s.nbVariables, 4)
        expected = Array(testMatrix2FirstPhase)
        for i in range(len(expected)):
            self.assertEqual(s.tableaux[i], expected[i], "(row %d)" % i)
        s.removeVariable()
        self.assertEqual(s.nbVariables, 3)
        for i in range(len(expected)):
            self.assertEqual(s.tableaux[i], testMatrix2[i], "(row %d)" % i)

    def testRemoveBasicVariable(self):
        s = Simplex(Array([
            [0, -1, -1, 0, 0],
            [1, -1, +1, 0, 0],
            [0, -1, -1, 1, 2]
        ]))
        s.basicVariables = [None, 0, 3]
        expected = Array([
            [0, -2, 0, 0],
            [1, -1, 0, 0],
            [0, -2, 1, 2]
        ])
        s.removeVariable()
        for i in range(len(expected)):
            self.assertEqual(s.tableaux[i], expected[i], "(row %d)" % i)
        self.assertEqual(s.basicVariables[1:], [0, 2])

    def testSolve(self):
        s = Simplex(testMatrix1)
        s.variableFromIndex = {i : str(i) for i in range(s.nbVariables)}
        objective = s.tableaux[0].copy()
        s.tableaux[0] = s.tableaux[0].__class__(([0]*len(s.tableaux[0])))
        s.addVariable()
        row, value = s.firstPhaseLeavingVariable()
        self.assertEqual(row, 2)
        s.performPivot(row, 0)
        expected = Array([
            [F(0), F(-1), F(1), F(-1), F(0), F(0), F(1), F(-10)],
            [F(0), F(5), F(-3), F(2), F(-1), F(1), F(-1), F(8)],
            [F(1), F(1), F(-1), F(1), F(0), F(0), F(-1), F(10)],
        ])
        for i in range(len(expected)):
            self.assertEqual(s.tableaux[i], expected[i], "(row %d)" % i)
        row, column = 1, 3
        s.performPivot(row, column)
        expected = Array([
            [F(0), F(3, 2), F(-1, 2), F(0), F(-1, 2), F(1, 2), F(1, 2), F(-6)],
            [F(0), F(5, 2), F(-3, 2), F(1), F(-1, 2), F(1, 2), F(-1, 2), F(4)],
            [F(1), F(-3, 2), F(1, 2), F(0), F(1, 2), F(-1, 2), F(-1, 2), F(6)],
        ])
        for i in range(len(expected)):
            self.assertEqual(s.tableaux[i], expected[i], "(row %d)" % i)
        row, column = 2, 2
        s.performPivot(row, column)
        expected = Array([
            [F(1), F(0), F(0), F(0), F(0), F(0), F(0), F(0)],
            [F(3), F(-2), F(0), F(1), F(1), F(-1), F(-2), F(22)],
            [F(2), F(-3), F(1), F(0), F(1), F(-1), F(-1), F(12)],
        ])
        for i in range(len(expected)):
            self.assertEqual(s.tableaux[i], expected[i], "(row %d)" % i)
        s.removeVariable()
        s.tableaux[0] = objective
        s.updateObjective()
        expected = Array([
            [F(1), F(0), F(0), F(1), F(0), F(2), F(-20)],
            [F(-2), F(0), F(1), F(1), F(-1), F(-2), F(22)],
            [F(-3), F(1), F(0), F(1), F(-1), F(-1), F(12)],
        ])
        for i in range(len(expected)):
            self.assertEqual(s.tableaux[i], expected[i], "(row %d)" % i)

    def testSolve2(self):
        s = Simplex(Array(testMatrix1))
        s.variableFromIndex = {i : str(i) for i in range(s.nbVariables)}
        opt, optSol = s.solve()
        self.assertEqual(opt, -20)
        self.assertEqual(optSol, {
            '0' : 0,
            '1' : 12,
            '2' : 22,
            '3' : 0
        })
        s = Simplex(testMatrix2)
        s.variableFromIndex = {i : str(i) for i in range(s.nbVariables)}
        opt, optSol = s.solve()
        self.assertEqual(opt, 13)
        self.assertEqual(optSol, {
            '0' : 2,
            '1' : 0,
            '2' : 1
        })

    def testTrivialEmpty(self):
        """
            Maximize 0 st x_0 <= 3 AND x_0 >= 4
        """
        s = Simplex(Array([
            [F(0), F(0), F(0), F(0)],
            [F(1), F(1), F(0), F(3)],
            [F(-1), F(0), F(1), F(-4)]
        ]))
        s.variableFromIndex = {i : str(i) for i in range(s.nbVariables)}
        with self.assertRaises(Empty):
            s.solve()

    def testTrivialUnbounded(self):
        """
            Maximize x_0 st x_0 >= 4
        """
        s = Simplex(Array([
            [F(-1), F(0), F(0)],
            [F(-1), F(1),F(-4)]
        ]))
        s.variableFromIndex = {i : str(i) for i in range(s.nbVariables)}
        with self.assertRaises(Unbounded):
            s.solve()
