class Literal:
    """
        Represents a literal: a variable (a string) with a factor (a fraction).
    """
    def __init__(self, factor, variable):
        self.factor = factor
        self.variable = variable

    def __repr__(self):
        return '%s%s' % (self.factor, self.variable)

class Expression:
    """
        Represents an expression: a sum of literals which is between two (or less)
        bounds.
    """
    def __init__(self, leftBound=None, rightBound=None, expression=None):
        self.leftBound = leftBound
        self.rightBound = rightBound
        self.expression = expression

    def __repr__(self):
        left = "" if self.leftBound is None else "%s <= " % self.leftBound
        right = "" if self.rightBound is None else "<= %s" % self.rightBound
        return "%s%s%s" % (left, " ".join(self.expression), right)

class LinearProgram:

    def __init__(self):
        self.objective = None
        self.subjectTo = []
        self.bounds = []
