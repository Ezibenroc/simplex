from fractions import Fraction
import numpy
from .simplex import Simplex, Unbounded, Empty

class Literal:
    """
        Represents a literal: a variable (a string) with a factor (a fraction).
    """
    def __init__(self, factor, variable):
        self.factor = factor
        self.variable = variable

    def __repr__(self):
        return '%s%s' % (self.factor, self.variable)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return str(self).__hash__()

    def copy(self):
        return self.__class__(self.factor, self.variable)

    def copyInv(self):
        return self.__class__(-self.factor, self.variable)

class Expression:
    """
        Represents an expression: a sum of literals which is between two (or less)
        bounds.
    """
    def __init__(self, leftBound=None, rightBound=None, literalList=None, constantTerm=0):
        self.leftBound = leftBound
        self.rightBound = rightBound
        self.literalList = literalList
        self.constantTerm = constantTerm

    def __repr__(self):
        left = "" if self.leftBound is None else "%s <= " % self.leftBound
        right = "" if self.rightBound is None else "<= %s" % self.rightBound
        constant = "" if self.constantTerm == 0 else (" +%s" % self.constantTerm if self.constantTerm > 0 else " %s"%self.constantTerm)
        return "%s%s%s%s" % (left, " ".join(str(x) for x in self.literalList), constant, right)

    def __eq__(self, other):
        if self.leftBound != other.leftBound or self.rightBound != other.rightBound or self.constantTerm != other.constantTerm:
            return False
        return set(self.literalList) == set(other.literalList)

    def normalForm(self):
        """
            Return a list of equivalent expressions, such that each expression is
            in canonical form (no left bound).
        """
        left, right = None, None
        if not self.rightBound is None:
            right = Expression(None, self.rightBound, [lit.copy() for lit in self.literalList], self.constantTerm)
        if not self.leftBound is None:
            left = Expression(None, -self.leftBound, [lit.copyInv() for lit in self.literalList], -self.constantTerm)
        return [x for x in [left, right] if not x is None]

class Variable:
    """
        Represents a variable (given by a string) and the transformations made
        to it during the normalization (eventual multiplication by -1, eventual
        addition of some constant).
    """
    def __init__(self, name, mult=1, add=0):
        self.name = name
        self.mult = mult
        self.add = add

    def __repr__(self):
        return '(%s: %d, %d)' % (self.name, self.mult, self.add)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def invert(self):
        self.mult = -self.mult

    def translate(self, n):
        self.add += n

    def computeValue(self, n):
        return (n-self.add)*self.mult

class LinearProgram:
    def __init__(self):
        self.objective = None
        self.objectiveFunction = None
        self.subjectTo = []
        self.bounds = []
        self.variables = {}

    def check(self):
        for expr, lineno in self.subjectTo + self.bounds:
            if (not expr.leftBound is None and not expr.rightBound is None and
                    expr.leftBound > expr.rightBound):
                raise Exception('Error at line %s: impossible bounds.' % lineno)
            for lit in expr.literalList:
                if not lit.variable in self.variables:
                    raise Exception('Error at line %s: unknown variable %s.' % (lineno, lit.variable))
        for lit in self.objectiveFunction[0].literalList:
            if not lit.variable in self.variables:
                raise Exception('Error at line %s: unknown variable %s.' % (self.objectiveFunction[1], lit.variable))
        for expr, lineno in self.bounds:
            if expr.leftBound is None and expr.rightBound is None:
                raise Exception('Error at line %s: unbounded variable %s.' % (lineno, expr.literalList[0].variable))
        self.objectiveFunction = self.objectiveFunction[0]
        self.subjectTo = [x[0] for x in self.subjectTo]
        self.bounds = [x[0] for x in self.bounds]

    def invertVariable(self, variableName):
        """
            invert(x_1): x'_1:= -x_1 so x_1=-x'_1
        """
        self.variables[variableName].invert()
        for expr in self.subjectTo + [self.objectiveFunction]:
            for lit in expr.literalList:
                if lit.variable == variableName:
                    lit.factor = -lit.factor
                    break

    def translateVariable(self, variableName, n):
        """
            translate(x_1, n): x'_1:= x_1+n so x_1=x'_1-n
        """
        self.variables[variableName].translate(n)
        for expr in self.subjectTo + [self.objectiveFunction]:
            for lit in expr.literalList:
                if lit.variable == variableName:
                    expr.constantTerm -= lit.factor*n
                    break

    def normalizeBounds(self):
        for expr in self.bounds:
            if not expr.rightBound is None and (expr.rightBound <= 0 or expr.leftBound is None):
                self.invertVariable(expr.literalList[0].variable)
                expr.leftBound, expr.rightBound = -expr.rightBound, (-expr.leftBound if not expr.leftBound is None else None)
            if expr.leftBound != 0:
                self.translateVariable(expr.literalList[0].variable, -expr.leftBound)
                expr.leftBound, expr.rightBound = 0, (expr.rightBound - expr.leftBound if not expr.rightBound is None else None)
            if not expr.rightBound is None:
                self.subjectTo.append(Expression(None, expr.rightBound, expr.literalList))

    def normalizeConstraints(self):
        self.subjectTo = [subexpr for expr in self.subjectTo for subexpr in expr.normalForm()]

    def replaceUnconstrained(self, var):
        v1 = '_0_'+var
        v2 = '_1_'+var
        self.variables.pop(var)
        self.variables[v1] = Variable(v1)
        self.variables[v2] = Variable(v2)
        l = list(filter(lambda lit: lit.variable == var, self.objectiveFunction.literalList))
        if l: # the variable is in the objective function
            self.objectiveFunction.literalList = list(filter(lambda lit: lit.variable != var, self.objectiveFunction.literalList))\
                + [Literal(l[0].factor, v1), Literal(-l[0].factor, v2)]
        for expr in self.subjectTo:
            l = list(filter(lambda lit: lit.variable == var, expr.literalList))
            if l: # the variable is in the objective function
                expr.literalList = list(filter(lambda lit: lit.variable != var, expr.literalList))\
                    + [Literal(l[0].factor, v1), Literal(-l[0].factor, v2)]
        return v1, v2

    def pullUnconstrainedVariables(self):
        varBounds = set(expr.literalList[0].variable for expr in self.bounds)
        var = set(self.variables)
        unconstrained = var-varBounds
        self.unconstrained = {}
        for v in unconstrained:
            v1, v2 = self.replaceUnconstrained(v)
            self.unconstrained[v] = v1, v2

    def pushUnconstrainedVariables(self, solution):
        for var, (v1, v2) in self.unconstrained.items():
            assert(solution[v1] == 0 or solution[v2] == 0)
            self.variables[var] = Variable(var)
            if solution[v1] != 0:
                solution[var] = solution[v1]
            else:
                solution[var] = -solution[v2]
            solution.pop(v1)
            solution.pop(v2)

    def normalize(self):
        self.normalizeBounds()
        self.normalizeConstraints()
        self.pullUnconstrainedVariables()

    def initSimplex(self):
        """
            Add a simplex attribute corresponding to the linear program.
        """
        nbVariables = len(self.variables)
        nbConstraints = len(self.subjectTo)
        tableaux = numpy.array([[Fraction(0, 1)]*(nbVariables + nbConstraints + 1)\
            for i in range(nbConstraints + 1)])
        variableFromIndex, indexFromVariable = {}, {}
        for i, var in enumerate(sorted(self.variables)):
            variableFromIndex[i] = var
            indexFromVariable[var] = i
        for v in range(nbVariables, nbVariables + nbConstraints):
            variableFromIndex[v] = '_slack_%d' % (v-nbVariables)
            indexFromVariable['_slack_%d' % (v-nbVariables)] = v
        objFactor = -1 if self.objective == 'MAXIMIZE' else 1
        for lit in self.objectiveFunction.literalList:
            tableaux[0][indexFromVariable[lit.variable]] = objFactor*lit.factor
        tableaux[0][-1] = -objFactor*self.objectiveFunction.constantTerm
        for constraint, expr in enumerate(self.subjectTo):
            for lit in expr.literalList:
                tableaux[constraint+1][indexFromVariable[lit.variable]] = lit.factor
            tableaux[constraint+1][nbVariables+constraint] = Fraction(1)
            tableaux[constraint+1][-1] = expr.rightBound-expr.constantTerm
        self.simplex = Simplex(tableaux)
        self.simplex.basicVariables = [None]+list(range(nbVariables, nbVariables+nbConstraints))
        self.simplex.variableFromIndex = variableFromIndex
        self.simplex.indexFromVariable = indexFromVariable

    def solve(self, verbose=False):
        self.initSimplex()
        try:
            opt, optSol = self.simplex.solve(verbose)
        except Unbounded:
            print("No optimal solution (unbounded).")
            return
        except Empty:
            print("No optimal solution (empty).")
            return
        self.pushUnconstrainedVariables(optSol)
        print("Optimal solution: %d." % opt)
        print("Found with the following affectation of the variables:")
        for var in sorted(optSol):
            print("%s = %s" % (var, self.variables[var].computeValue(optSol[var])))
