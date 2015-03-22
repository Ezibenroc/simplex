from fractions import Fraction
from parser import Parser

class LinearProgram:

    def __init__(self):
        self.nbVariables = 0
        self.nbConstraints = 0
        self.objective = None
        self.tableaux = None
        self.variableFromIndex = {}
        self.indexFromVariable = {}

    def __str__(self):
        return '\n'.join(' '.join(str(y) for y in x) for x in self.tableaux.tolist())

if __name__ == '__main__':
    lp = LinearProgram()
    parser = Parser(lp, 'example.in')
    parser.parse()
    print(lp.variableFromIndex)
    print(lp.indexFromVariable)
    print(lp.nbVariables)
    print(lp.nbConstraints)
    print(lp)
