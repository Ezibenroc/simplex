from fractions import Fraction
from .parser import Parser

class EndOfAlgorithm(Exception):
    pass

class Unbounded(Exception):
    pass

class LinearProgram:

    def __init__(self, tableaux = None):
        self.tableaux = tableaux
        if not self.tableaux is None:
            self.nbConstraints = len(self.tableaux.A) - 1
            self.nbVariables = len(self.tableaux.A[0]) - self.nbConstraints - 2
        else:
            self.nbVariables = 0
            self.nbConstraints = 0
        self.objective = None
        self.variableFromIndex = {}
        self.indexFromVariable = {}

    def __str__(self):
        return '\n'.join(' '.join(str(y).ljust(6) for y in x) for x in self.tableaux.tolist())

    def chosePivot(self):
        column = self.tableaux[0].argmax()
        if self.tableaux[0, column] < 0:
            raise EndOfAlgorithm
        row = None
        for r in range(1, self.nbConstraints):
            if self.tableaux[r, column] < 0:
                if row is None:
                    row = r
                elif -self.tableaux[r, -1]/self.tableaux[r, column] < -self.tableaux[row, -1]/self.tableaux[row, column]:
                    row = r
        if row is None:
            raise Unbounded

if __name__ == '__main__':
    lp = LinearProgram()
    parser = Parser(lp, 'example.in')
    parser.parse()
    print(lp.variableFromIndex)
    print(lp.indexFromVariable)
    print(lp.nbVariables)
    print(lp.nbConstraints)
    print(lp)
    print(lp.chosePivot())
