from fractions import Fraction
from parser import Parser

class LinearProgram:

    def __init__(self):
        self.nbVariables = 0
        self.nbConstraints = 0
        self.tableaux = None
        self.variableFromIndex = {}
        self.indexFromVariable = {}

if __name__ == '__main__':
    lp = LinearProgram()
    parser = Parser(lp, 'example.in')
    parser.parse()
    print(lp.variableFromIndex)
    print(lp.indexFromVariable)
