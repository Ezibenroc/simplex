from fractions import Fraction
import numpy as np
from .parser import Parser

class EndOfAlgorithm(Exception):
    pass

class Unbounded(Exception):
    pass

class LinearProgram:

    def __init__(self, tableaux = None):
        if not tableaux is None:
            self.tableaux = np.matrix(tableaux)
            self.nbConstraints = len(self.tableaux.A) - 1
            self.nbVariables = len(self.tableaux.A[0]) - self.nbConstraints - 1
        else:
            self.tableaux = None
            self.nbVariables = 0
            self.nbConstraints = 0
        self.objective = None
        self.variableFromIndex = {}
        self.indexFromVariable = {}

    def __str__(self):
        return '\n'.join(' '.join(str(y).ljust(6) for y in x) for x in self.tableaux.tolist())

    def chosePivot(self):
        column = self.tableaux[0].argmax()
        if column == len(self.tableaux.A[0]) -1 or self.tableaux[0, column] <= 0:
            raise EndOfAlgorithm
        row = None
        for r in range(1, self.nbConstraints):
            if self.tableaux[r, column] < 0:
                if row is None:
                    row = r
                elif -self.tableaux[r, -1]/self.tableaux[r, column] < -self.tableaux[row, -1]/self.tableaux[row, column]:
                    row = r
        if row is None:
            raise Unbounded('Variable %d' % column)
        return row, column

    def performPivot(self, row, column):
        self.tableaux[row]/=self.tableaux[row, column]
        for r in range(len(self.tableaux)):
            if r != row:
                coeff = self.tableaux[r, column]
                for c in range(len(self.tableaux.A[0])):
                    self.tableaux[r, c] -= coeff*self.tableaux[row, c]

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
