from fractions import Fraction
import numpy as np
from .parser import Parser

class EndOfAlgorithm(Exception):
    pass

class Unbounded(Exception):
    pass

class Empty(Exception):
    pass

class LinearProgram:

    def __init__(self, tableaux = None):
        if not tableaux is None:
            self.tableaux = np.array(tableaux)
            self.nbConstraints = len(self.tableaux) - 1
            self.nbVariables = len(self.tableaux[0]) - self.nbConstraints - 1
            self.basicVariables = [None]+list(range(self.nbVariables, self.nbVariables+self.nbConstraints))
        else:
            self.tableaux = None
            self.nbVariables = 0
            self.nbConstraints = 0
            self.basicVariables = [None]
        self.objective = None
        self.variableFromIndex = {}
        self.indexFromVariable = {}

    def __str__(self):
        return '\n'.join(' '.join(str(y).ljust(6) for y in x) for x in self.tableaux.tolist())

    def chosePivot(self):
        column = self.tableaux[0][:-1].argmin()
        if column == len(self.tableaux[0]) -1 or self.tableaux[0][column] >= 0:
            raise EndOfAlgorithm
        row = None
        for r in range(1, len(self.tableaux)):
            if self.tableaux[r, column] > 0:
                if row is None:
                    row = r
                elif self.tableaux[r][-1]/self.tableaux[r][column] < self.tableaux[row][-1]/self.tableaux[row][column]:
                    row = r
        if row is None:
            raise Unbounded('Variable %d' % column)
        return row, column

    def performPivot(self, row, column):
        self.basicVariables[row] = column
        self.tableaux[row]/=self.tableaux[row][column]
        for r in range(len(self.tableaux)):
            if r != row:
                coeff = self.tableaux[r][column]
                for c in range(len(self.tableaux[0])):
                    self.tableaux[r][c] -= coeff*self.tableaux[row][c]

    def runSimplex(self):
        while(True):
            try:
                row, column = self.chosePivot()
            except EndOfAlgorithm:
                break
            self.performPivot(row, column)
        return self.tableaux[0][-1]

    def addVariable(self):
        self.tableaux = np.hstack(([[Fraction(-1)] for i in range(len(self.tableaux))], self.tableaux))
        self.tableaux[0][0] = Fraction(1)
        self.basicVariables = [None] + [0]*self.nbConstraints
        self.nbVariables += 1

    def removeVariable(self):
        self.tableaux = np.delete(self.tableaux, 0, 1)
        self.nbVariables -= 1
        self.basicVariables = [None]+[x-1 for x in self.basicVariables[1:]]

    def firstPhaseLeavingVariable(self):
        imin = 1
        for i in range(2, len(self.tableaux)):
            if self.tableaux[i][-1] < self.tableaux[imin][-1]:
                imin = i
        return imin

    def updateObjective(self):
        for row, column in enumerate(self.basicVariables):
            if column is None:
                continue
            self.tableaux[0] -= self.tableaux[0][column]*self.tableaux[row]

    def solve(self):
        objective = list(self.tableaux[0])
        self.tableaux[0] = [0]*len(self.tableaux[0])
        self.addVariable()
        self.performPivot(self.firstPhaseLeavingVariable(), 0)
        if self.runSimplex() != 0:
            raise Empty
        self.removeVariable()
        for i, col in enumerate(objective):
            self.tableaux[0][i] = objective[i]
        self.updateObjective()
        return self.runSimplex()
