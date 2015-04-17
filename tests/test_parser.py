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

    def testParseLine(self):
        p = Parser(None, None)
        expr = p.parseLine('literals<=4/3')
        self.assertEqual(expr.literalList, [Literal(1, 'literals')])
        self.assertEqual(expr.leftBound, None)
        self.assertEqual(expr.rightBound, F(4, 3))
        expr = p.parseLine('literals>=4/3')
        self.assertEqual(expr.literalList, [Literal(1, 'literals')])
        self.assertEqual(expr.leftBound, F(4, 3))
        self.assertEqual(expr.rightBound, None)
        expr = p.parseLine('3>=literals>=4/3')
        self.assertEqual(expr.literalList, [Literal(1, 'literals')])
        self.assertEqual(expr.leftBound, F(4, 3))
        self.assertEqual(expr.rightBound, 3)
        expr = p.parseLine('-3<=literals<=4/3')
        self.assertEqual(expr.literalList, [Literal(1, 'literals')])
        self.assertEqual(expr.leftBound, -3)
        self.assertEqual(expr.rightBound, F(4, 3))
        expr = p.parseLine('literals=4/3')
        self.assertEqual(expr.literalList, [Literal(1, 'literals')])
        self.assertEqual(expr.leftBound, F(4, 3))
        self.assertEqual(expr.rightBound, F(4, 3))

    def testParse(self):
        lp = LinearProgram()
        p = Parser(lp, 'tests/example2.in')
        p.parse()
        self.assertEqual(lp.objective, 'MAXIMIZE')
        self.assertEqual(lp.objectiveFunction, Expression(None, None, [
            Literal(5, 'x_1'),
            Literal(4, 'x_2'),
            Literal(3, 'x_3')
        ]))
        self.assertEqual(len(lp.subjectTo), 3)
        self.assertIn(Expression(None, 5, [
            Literal(2, 'x_1'),
            Literal(3, 'x_2'),
            Literal(1, 'x_3')
        ]), lp.subjectTo)
        self.assertIn(Expression(None, 11, [
            Literal(4, 'x_1'),
            Literal(1, 'x_2'),
            Literal(2, 'x_3')
        ]), lp.subjectTo)
        self.assertIn(Expression(None, 8, [
            Literal(3, 'x_1'),
            Literal(4, 'x_2'),
            Literal(2, 'x_3')
        ]), lp.subjectTo)
        self.assertEqual(len(lp.bounds), 3)
        for v in ['x_1', 'x_2', 'x_3']:
            self.assertIn(Expression(0, None, [Literal(1, v)]), lp.bounds)
        self.assertEqual(len(lp.variables), 3)
        self.assertEqual(set(lp.variables), set(['x_1', 'x_2', 'x_3']))
