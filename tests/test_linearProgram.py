from simplex import Literal, Expression, Variable, LinearProgram

from unittest import TestCase
import numpy as np
from fractions import Fraction as F

def getLP():
    lp = LinearProgram()
    lp.variables = {'x_1': Variable('x_1'), 'x_2': Variable('x_2')}
    lp.bounds = [
        Expression(-3, -1, [Literal(1, 'x_1')]),
        Expression(4, 9, [Literal(1, 'x_2')])
    ]
    lp.objective = Expression(None, None, [Literal(4, 'x_1'), Literal(-2, 'x_2')])
    lp.subjectTo = [
        Expression(None, 4, [Literal(-2, 'x_1'), Literal(F(-1, 3), 'x_2')]),
        Expression(F(1, 9), None, [Literal(3, 'x_1'), Literal(1, 'x_2')])
    ]
    return lp


class LinearProgramTests(TestCase):

    def testVariableTransformation(self):
        lp = getLP()
        lp.invertVariable('x_1')
        lp.translateVariable('x_2', 3)
        self.assertEqual(lp.objective, Expression(None, None, [Literal(-4, 'x_1'), Literal(-2, 'x_2')], 6))
        self.assertEqual(lp.subjectTo, [
            Expression(None, 4, [Literal(2, 'x_1'), Literal(F(-1, 3), 'x_2')], 1),
            Expression(F(1, 9), None, [Literal(-3, 'x_1'), Literal(1, 'x_2')], -3)
        ])

    def testNormalizeBounds(self):
        lp = getLP()
        lp.normalizeBounds()
        self.assertEqual(lp.variables, {
            'x_1' : Variable('x_1', -1, -1),
            'x_2' : Variable('x_2', 1, -4)
        })
        self.assertEqual(lp.bounds, [
            Expression(0, 2, [Literal(1, 'x_1')]),
            Expression(0, 5, [Literal(1, 'x_2')])
        ])
        self.assertEqual(lp.objective, Expression(None, None, [Literal(-4, 'x_1'), Literal(-2, 'x_2')], -12))
        self.assertEqual(lp.subjectTo, [
            Expression(None, 4, [Literal(2, 'x_1'), Literal(F(-1, 3), 'x_2')], F(2, 3)),
            Expression(F(1, 9), None, [Literal(-3, 'x_1'), Literal(1, 'x_2')], 1),
            Expression(None, 2, [Literal(1, 'x_1')]),
            Expression(None, 5, [Literal(1, 'x_2')])
        ])
