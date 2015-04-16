from simplex import Literal, Expression, LinearProgram, Parser

from unittest import TestCase
import numpy as np
from fractions import Fraction as F

class ParserTests(TestCase):

    def testParseLiteralList(self):
        p = Parser(None, None)
        self.assertEqual(p.parseLiteralList('x_5', None), [Literal(1, 'x_5')])
        l = p.parseLiteralList('2azerty-3/2AzErTy-A_z_E_r_T_y+A_2___151_3a_5_y', None)
        self.assertEqual(len(l), 4)
        self.assertIn(Literal(2, 'azerty'), l)
        self.assertIn(Literal(F(-3, 2), 'AzErTy'), l)
        self.assertIn(Literal(-1, 'A_z_E_r_T_y'), l)
        self.assertIn(Literal(1, 'A_2___151_3a_5_y'), l)
