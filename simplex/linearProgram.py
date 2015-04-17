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

class Expression:
    """
        Represents an expression: a sum of literals which is between two (or less)
        bounds.
    """
    def __init__(self, leftBound=None, rightBound=None, literalList=None):
        self.leftBound = leftBound
        self.rightBound = rightBound
        self.literalList = literalList

    def __repr__(self):
        left = "" if self.leftBound is None else "%s <= " % self.leftBound
        right = "" if self.rightBound is None else "<= %s" % self.rightBound
        return "%s%s%s" % (left, " ".join(str(x) for x in self.literalList), right)

    def __eq__(self, other):
        if self.leftBound != other.leftBound or self.rightBound != other.rightBound:
            return False
        return set(self.literalList) == set(other.literalList)

class LinearProgram:
    def __init__(self):
        self.objective = None
        self.objectiveFunction = None
        self.subjectTo = []
        self.bounds = []
        self.variables = []

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
        self.objectiveFunction = self.objectiveFunction[0]
        self.subjectTo = [x[0] for x in self.subjectTo]
        self.bounds = [x[0] for x in self.bounds]
