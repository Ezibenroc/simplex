from simplex import LinearProgram, EndOfAlgorithm, Unbounded

from unittest import TestCase
import numpy as np
from fractions import Fraction as F

testMatrix = np.matrix([
    [F(1), F(-3), F(2), F(-2), F(-4), F(0), F(0), F(0)],
    [F(0), F(4), F(-2), F(1), F(-1), F(1), F(0), F(-2)],
    [F(0), F(-1), F(1), F(-1), F(0), F(0), F(1), F(-10)],
])

class StructureTests(TestCase):

    def testConstructor(self):
        lp = LinearProgram(testMatrix)
        self.assertEqual(lp.nbConstraints, 2)
        self.assertEqual(lp.nbVariables, 4)
