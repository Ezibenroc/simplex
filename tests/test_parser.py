from simplex import Simplex, EndOfAlgorithm, Unbounded, Parser

from unittest import TestCase
import numpy as np
from fractions import Fraction as F

testMatrix = np.array([
    [F(-5), F(-4), F(-3), F(0), F(0), F(0), F(0)],
    [F(2), F(3), F(1), F(1), F(0), F(0), F(5)],
    [F(4), F(1), F(2), F(0), F(1), F(0), F(11)],
    [F(3), F(4), F(2), F(0), F(0), F(1), F(8)],
])

class StructureTests(TestCase):

    def testSimpleParser(self):
        s = Simplex()
        parser = Parser(s, 'example2.in')
        parser.parse()
        self.assertEqual(s.nbVariables, 3)
        self.assertEqual(s.nbConstraints, 3)
        self.assertEqual(s.basicVariables[1:], [3, 4, 5])
        self.assertEqual(s.variableFromIndex, {
            0 : 'x_1',
            1 : 'x_2',
            2 : 'x_3',
            3 : '_slack_0',
            4 : '_slack_1',
            5 : '_slack_2',
        })
        self.assertEqual(s.indexFromVariable, {
            'x_1' : 0,
            'x_2' : 1,
            'x_3' : 2,
            '_slack_0' : 3,
            '_slack_1' : 4,
            '_slack_2' : 5,
        })
        for i in range(len(testMatrix)):
            np.testing.assert_array_equal(s.tableaux[i], testMatrix[i], "(row %d)" % i)
