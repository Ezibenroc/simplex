from fractions import Fraction
from .array import Array

class EndOfAlgorithm(Exception):
    '''
        The algorithm stopped on an optimal solution.
    '''
    pass

class Unbounded(Exception):
    '''
        There is no optimal solution (unbounded).
    '''
    pass

class Empty(Exception):
    '''
        There is no optimal solution (empty).
    '''
    pass

def latexWrap(string):
    return string.replace('_', '\_')

class Simplex:
    '''
        A class to run the simplex algorithm.
        Uses the tableaux representation.
    '''

    def __init__(self, tableaux = None):
        if not tableaux is None:
            self.tableaux = Array(tableaux)
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
            '\n'.join(' '.join(str(self.tableaux[i][j]).ljust(6) for j in range(len(self.tableaux[i]))) for i in range(len(self.tableaux)))
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

    def entryToString(self, entryID, avoid = None, sep = ' '):
        return sep.join('%s%s' % (self.fractionToString((-1 if avoid is None or i < len(self.tableaux[0])-1 else 1)*self.tableaux[entryID][i]),
                            latexWrap(self.variableFromIndex.get(i, '')))
                        for i in range(len(self.tableaux[0])) if i != avoid and self.tableaux[entryID][i] != 0)

    def __str__(self, sep = ' '):
        return '\n'.join([
            'MAXIMIZE',
            self.entryToString(0),
            'SUBJECT TO'
        ] + [
            '%s = %s' % (self.variableFromIndex[self.basicVariables[i]],
                self.entryToString(i, self.basicVariables[i], sep)) for i in range(1, len(self.tableaux))
        ])

    def toLatex(self):
        return '\\begin{align*}\n%s\n\\end{align*}\n\n' % ('\n'.join([
            '\\text{Maximize}\\\\',
            '&%s\\\\' % self.entryToString(0),
            '\\text{Subject to}\\\\'
        ] + [
            '%s &= %s\\\\' % (latexWrap(self.variableFromIndex[self.basicVariables[i]]),
                self.entryToString(i, self.basicVariables[i])) for i in range(1, len(self.tableaux))
        ]))

    def choosePivot(self):
        '''
            Choose the entering and leaving variables.
        '''
        column = self.tableaux[0].argmin(0, -1)
        if column == len(self.tableaux[0]) -1 or self.tableaux[0][column] >= 0:
            raise EndOfAlgorithm
        row = None
        for r in range(1, len(self.tableaux)):
            if self.tableaux[r][column] > 0:
                if row is None:
                    row = r
                elif self.tableaux[r][-1]/self.tableaux[r][column] < self.tableaux[row][-1]/self.tableaux[row][column]:
                    row = r
        if row is None:
            raise Unbounded('Variable %d' % column)
        return row, column

    def performPivot(self, row, column, verbose = False, latex=None):
        '''
            Perform a pivot, given the entering and leaving variables.
        '''
        if verbose:
            print('Entering variable: %s' % self.variableFromIndex[column])
            print('Leaving variable: %s' % self.variableFromIndex[self.basicVariables[row]])
        if latex:
            latex.write('Entering variable: $%s$\n\n' % latexWrap(self.variableFromIndex[column]))
            latex.write('Leaving variable: $%s$\n\n' % latexWrap(self.variableFromIndex[self.basicVariables[row]]))
        self.basicVariables[row] = column
        self.tableaux[row]/=self.tableaux[row][column]
        for r in range(len(self.tableaux)):
            if r != row:
                coeff = self.tableaux[r][column]
                self.tableaux[r] -= coeff*self.tableaux[row]
        if verbose:
            print(self, '\n')
        if latex:
            latex.write(self.toLatex())

    def runSimplex(self, verbose = False, latex=None):
        '''
            Run the basic simplex (without first phase).
        '''
        while(True):
            try:
                row, column = self.choosePivot()
            except EndOfAlgorithm:
                break
            self.performPivot(row, column, verbose, latex)
        return self.tableaux[0][-1]

    def addVariable(self):
        '''
            Add a new variable.
        '''
        self.tableaux.addColumn(Fraction(-1))
        self.tableaux[0][0] = Fraction(1)
        self.basicVariables = [None]+[x+1 for x in self.basicVariables[1:]]
        self.nbVariables += 1
        self.variableFromIndex = {i+1:var for i, var in self.variableFromIndex.items()}
        self.variableFromIndex[0] = '_phase1_'
        self.indexFromVariable = {var:i+1 for var, i in self.indexFromVariable.items()}
        self.indexFromVariable['_phase1_'] = 0

    def removeVariable(self):
        '''
            Remove the variable which was added by addVariable.
        '''
        if 0 in self.basicVariables:
            row = self.basicVariables.index(0)
            assert self.tableaux[row][-1] == 0
            column = 1
            while column < len(self.tableaux[row]) and self.tableaux[row][column] == 0:
                column += 1
            assert column < len(self.tableaux[row])
            self.performPivot(row, column)
        self.tableaux.removeColumn()
        self.nbVariables -= 1
        self.basicVariables = [None]+[x-1 for x in self.basicVariables[1:]]
        self.variableFromIndex = {i-1:var for i, var in self.variableFromIndex.items() if i != 0}
        self.indexFromVariable = {var:i-1 for var, i in self.indexFromVariable.items() if i != 0}

    def firstPhaseLeavingVariable(self):
        '''
            Choose the leaving variable of the first phase's first pivot.
        '''
        imin = 1
        for i in range(2, len(self.tableaux)):
            if self.tableaux[i][-1] < self.tableaux[imin][-1]:
                imin = i
        return imin, self.tableaux[imin][-1]

    def updateObjective(self):
        '''
            Update the objective function after the first phase.
        '''
        for row, column in enumerate(self.basicVariables):
            if column is None:
                continue
            self.tableaux[0] -= self.tableaux[0][column]*self.tableaux[row]

    def solve(self, verbose = False, latex=None):
        '''
            Perform the whole simplex algorithm, first phase included.
        '''
        if verbose:
            print(self, '\n')
        if latex:
            latex.write(self.toLatex())
        firstPhaseVariable, constantValue = self.firstPhaseLeavingVariable()
        if verbose:
            print('\n\n# FIRST PHASE\n')
        if latex:
            latex.write('\\section*{First phase}\n\n')
        if constantValue < 0:
            objective = self.tableaux[0].copy()
            self.tableaux[0] = self.tableaux[0].__class__([0]*len(self.tableaux[0]))
            self.addVariable()
            if verbose:
                print(self, '\n')
            if latex:
                latex.write(self.toLatex())
            self.performPivot(firstPhaseVariable, 0, verbose, latex)
            if self.runSimplex(verbose, latex) != 0:
                raise Empty
            self.removeVariable()
            for i, col in enumerate(objective):
                self.tableaux[0][i] = objective[i]
            self.updateObjective()
            if verbose:
                print('Remove the variable and put back the objective function:')
                print(self, '\n')
            if latex:
                latex.write('Remove the variable and put back the objective function:\n')
                latex.write(self.toLatex())
        if verbose:
            print('\n\n# SECOND PHASE\n')
        if latex:
            latex.write('\\section*{Second phase}\n\n')
        opt = self.runSimplex(verbose, latex)
        optSol = {self.variableFromIndex[varID] : Fraction(0) for varID in range(self.nbVariables)}
        for constraint in range(1, self.nbConstraints+1):
            if self.basicVariables[constraint] < self.nbVariables: # not a slack variable
                optSol[self.variableFromIndex[self.basicVariables[constraint]]] = self.tableaux[constraint][-1]
        return opt, optSol
