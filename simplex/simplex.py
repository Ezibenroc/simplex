from fractions import Fraction
import numpy as np

class EndOfAlgorithm(Exception):
    pass

class Unbounded(Exception):
    pass

class Empty(Exception):
    pass

class Simplex:

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

    def __repr__(self):
        return '\n'.join([
            'nbConstraints: %d' % self.nbConstraints,
            'nbVariables: %d' % self.nbVariables,
            'basicVariables: %s' % self.basicVariables,
            'variableFromIndex: %s' % self.variableFromIndex,
            'indexFromVariable: %s' % self.indexFromVariable,
            '\n'.join(' '.join(str(y).ljust(6) for y in x) for x in self.tableaux.tolist())
        ])

    @staticmethod
    def fractionToString(f):
        if f == 1:
            return '+'
        elif f == -1:
            return '-'
        elif f > 0:
            return '+%s' % f
        else:
            return str(f)

    def entryToString(self, entryID, avoid = None):
        return ' '.join('%s%s' % (self.fractionToString((-1 if avoid is None or i < len(self.tableaux[0])-1 else 1)*self.tableaux[entryID][i]),
                            self.variableFromIndex.get(i, ''))
                        for i in range(len(self.tableaux[0])) if i != avoid and self.tableaux[entryID][i] != 0)

    def __str__(self):
        return '\n'.join([
            'MAXIMIZE',
            self.entryToString(0),
            'SUBJECT TO'
        ] + [
            '%s = %s' % (self.variableFromIndex[self.basicVariables[i]],
                self.entryToString(i, self.basicVariables[i])) for i in range(1, len(self.tableaux))
        ])

    def choosePivot(self):
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

    def performPivot(self, row, column, verbose = False):
        if verbose:
            print('Entering variable: %s' % self.variableFromIndex[column])
            print('Leaving variable: %s' % self.variableFromIndex[self.basicVariables[row]])
        self.basicVariables[row] = column
        self.tableaux[row]/=self.tableaux[row][column]
        for r in range(len(self.tableaux)):
            if r != row:
                coeff = self.tableaux[r][column]
                for c in range(len(self.tableaux[0])):
                    self.tableaux[r][c] -= coeff*self.tableaux[row][c]
        if verbose:
            print(self, "\n")

    def runSimplex(self, verbose = False):
        if verbose:
            print(self, "\n")
        while(True):
            try:
                row, column = self.choosePivot()
            except EndOfAlgorithm:
                break
            self.performPivot(row, column, verbose)
        return self.tableaux[0][-1]

    def addVariable(self):
        self.tableaux = np.hstack(([[Fraction(-1)] for i in range(len(self.tableaux))], self.tableaux))
        self.tableaux[0][0] = Fraction(1)
        self.basicVariables = [None]+[x+1 for x in self.basicVariables[1:]]
        self.nbVariables += 1
        self.variableFromIndex = {i+1:var for i, var in self.variableFromIndex.items()}
        self.variableFromIndex[0] = '_phase1_'
        self.indexFromVariable = {var:i+1 for var, i in self.indexFromVariable.items()}
        self.indexFromVariable['_phase1_'] = 0

    def removeVariable(self):
        if 0 in self.basicVariables:
            row = self.basicVariables.index(0)
            assert self.tableaux[row][-1] == 0
            column = 1
            while column < len(self.tableaux[row]) and self.tableaux[row][column] == 0:
                column += 1
            assert column < len(self.tableaux[row])
            self.performPivot(row, column)
        self.tableaux = np.delete(self.tableaux, 0, 1)
        self.nbVariables -= 1
        self.basicVariables = [None]+[x-1 for x in self.basicVariables[1:]]
        self.variableFromIndex = {i-1:var for i, var in self.variableFromIndex.items() if i != 0}
        self.indexFromVariable = {var:i-1 for var, i in self.indexFromVariable.items() if i != 0}

    def firstPhaseLeavingVariable(self):
        imin = 1
        for i in range(2, len(self.tableaux)):
            if self.tableaux[i][-1] < self.tableaux[imin][-1]:
                imin = i
        return imin, self.tableaux[imin][-1]

    def updateObjective(self):
        for row, column in enumerate(self.basicVariables):
            if column is None:
                continue
            self.tableaux[0] -= self.tableaux[0][column]*self.tableaux[row]

    def solve(self, verbose = False):
        if verbose:
            print(self)
        firstPhaseVariable, constantValue = self.firstPhaseLeavingVariable()
        if constantValue < 0:
            objective = list(self.tableaux[0])
            self.tableaux[0] = [0]*len(self.tableaux[0])
            self.addVariable()
            if verbose:
                print("\n\n# FIRST PHASE\n")
            self.performPivot(firstPhaseVariable, 0, verbose)
            if self.runSimplex(verbose) != 0:
                raise Empty
            self.removeVariable()
            for i, col in enumerate(objective):
                self.tableaux[0][i] = objective[i]
            self.updateObjective()
        if verbose:
            print("\n\n# SECOND PHASE\n")
        opt = self.runSimplex(verbose)
        optSol = {self.variableFromIndex[varID] : Fraction(0) for varID in range(self.nbVariables)}
        for constraint in range(1, self.nbConstraints+1):
            if self.basicVariables[constraint] < self.nbVariables: # not a slack variable
                optSol[self.variableFromIndex[self.basicVariables[constraint]]] = self.tableaux[constraint][-1]
        return opt, optSol
