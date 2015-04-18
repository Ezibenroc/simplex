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
    lp.objective = 'MAXIMIZE'
    lp.objectiveFunction = Expression(None, None, [Literal(4, 'x_1'), Literal(-2, 'x_2')])
    lp.subjectTo = [
        Expression(None, 4, [Literal(-2, 'x_1'), Literal(F(-1, 3), 'x_2')]),
        Expression(F(1, 9), None, [Literal(3, 'x_1'), Literal(1, 'x_2')]),
        Expression(F(27, 42), 11, [Literal(1, 'x_1'), Literal(1, 'x_2')])
    ]
    return lp

def getLP2():
    lp = LinearProgram()
    lp.variables = {'x_1': Variable('x_1'), 'x_2': Variable('x_2')}
    lp.bounds = [
        Expression(0, None, [Literal(1, 'x_1')]),
        Expression(0, None, [Literal(1, 'x_2')])
    ]
    lp.objective = 'MAXIMIZE'
    lp.objectiveFunction = Expression(None, None, [Literal(4, 'x_1'), Literal(-2, 'x_2')])
    lp.subjectTo = [
        Expression(None, 4, [Literal(-2, 'x_1'), Literal(F(-1, 3), 'x_2')]),
        Expression(0, 5, [Literal(3, 'x_1'), Literal(1, 'x_2')])
    ]
    return lp

def getLP3(): # same as LP2, but x_2 unconstrained
    lp = LinearProgram()
    lp.variables = {'x_1': Variable('x_1'), 'x_2': Variable('x_2')}
    lp.bounds = [
        Expression(0, None, [Literal(1, 'x_1')]),
    ]
    lp.objective = 'MAXIMIZE'
    lp.objectiveFunction = Expression(None, None, [Literal(4, 'x_1'), Literal(-2, 'x_2')])
    lp.subjectTo = [
        Expression(None, 4, [Literal(-2, 'x_1'), Literal(F(-1, 3), 'x_2')]),
        Expression(0, 5, [Literal(3, 'x_1'), Literal(1, 'x_2')])
    ]
    return lp

class LinearProgramTests(TestCase):

    def testVariableTransformation(self):
        lp = getLP()
        lp.invertVariable('x_1')
        lp.translateVariable('x_2', 3)
        self.assertEqual(lp.objectiveFunction, Expression(None, None, [Literal(-4, 'x_1'), Literal(-2, 'x_2')], 6))
        self.assertEqual(lp.subjectTo, [
            Expression(None, 4, [Literal(2, 'x_1'), Literal(F(-1, 3), 'x_2')], 1),
            Expression(F(1, 9), None, [Literal(-3, 'x_1'), Literal(1, 'x_2')], -3),
            Expression(F(27, 42), 11, [Literal(-1, 'x_1'), Literal(1, 'x_2')], -3)
        ])
        self.assertEqual(lp.variables['x_1'].computeValue(42), -42)
        self.assertEqual(lp.variables['x_2'].computeValue(42), 39)

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
        self.assertEqual(lp.objectiveFunction, Expression(None, None, [Literal(-4, 'x_1'), Literal(-2, 'x_2')], -12))
        self.assertEqual(lp.subjectTo, [
            Expression(None, 4, [Literal(2, 'x_1'), Literal(F(-1, 3), 'x_2')], F(2, 3)),
            Expression(F(1, 9), None, [Literal(-3, 'x_1'), Literal(1, 'x_2')], 1),
            Expression(F(27, 42), 11, [Literal(-1, 'x_1'), Literal(1, 'x_2')], 3),
            Expression(None, 2, [Literal(1, 'x_1')]),
            Expression(None, 5, [Literal(1, 'x_2')])
        ])
        self.assertEqual(lp.variables['x_1'].computeValue(1), -2)
        self.assertEqual(lp.variables['x_2'].computeValue(3), 7)

    def testNormalizeConstraints(self):
        lp = getLP()
        lp.normalizeConstraints()
        self.assertEqual(lp.subjectTo, [
            Expression(None, 4, [Literal(-2, 'x_1'), Literal(F(-1, 3), 'x_2')]),
            Expression(None, F(-1, 9), [Literal(-3, 'x_1'), Literal(-1, 'x_2')]),
            Expression(None, F(-27, 42), [Literal(-1, 'x_1'), Literal(-1, 'x_2')]),
            Expression(None, 11, [Literal(1, 'x_1'), Literal(1, 'x_2')])
        ])

    def testInitSimplex(self):
        lp = getLP2()
        lp.initSimplex()
        self.assertEqual(lp.simplex.nbVariables, 2)
        self.assertEqual(lp.simplex.nbConstraints, 2)
        self.assertEqual(lp.simplex.indexFromVariable, {
            'x_1' : 0,
            'x_2' : 1,
            '_slack_0' : 2,
            '_slack_1' : 3
        })
        self.assertEqual(lp.simplex.variableFromIndex, {
            0 : 'x_1',
            1 : 'x_2',
            2 : '_slack_0',
            3 : '_slack_1'
        })
        self.assertEqual(lp.simplex.basicVariables[1:], [2, 3])
        expected = np.array([
            [F(-4), F(2), F(0), F(0), F(0)],
            [F(-2), F(-1, 3), F(1), F(0), F(4)],
            [F(3), F(1), F(0), F(1), F(5)]
        ])
        for i in range(len(expected)):
            np.testing.assert_array_equal(lp.simplex.tableaux[i], expected[i], "(row %d)" % i)

    def testUnconstrained(self):
        lp = getLP3()
        lp.pullUnconstrainedVariables()
        self.assertEqual(len(lp.unconstrained), 1)
        self.assertIn('x_2', lp.unconstrained)
        v1, v2 = lp.unconstrained['x_2']
        self.assertIn(v1, lp.variables)
        self.assertIn(v2, lp.variables)
        self.assertNotIn('x_2', lp.variables)
        self.assertEqual(lp.objectiveFunction, Expression(None, None, [Literal(4, 'x_1'), Literal(-2, v1), Literal(2, v2)]))
        self.assertEqual(lp.subjectTo, [
            Expression(None, 4, [Literal(-2, 'x_1'), Literal(F(-1, 3), v1), Literal(F(1, 3), v2)]),
            Expression(0, 5, [Literal(3, 'x_1'), Literal(1, v1), Literal(-1, v2)])
        ])
        sol = {'x_1' : 3, v1 : 0, v2 : 4}
        lp.pushUnconstrainedVariables(sol)
        self.assertEqual(sol, {'x_1' : 3, 'x_2' : -4})
