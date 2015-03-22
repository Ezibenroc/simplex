from fractions import Fraction
import re

class Parser:
    OBJECTIVE = ['MINIMIZE', 'MAXIMIZE']
    SUBJECT_TO = 'SUBJECT TO'
    BOUNDS = 'BOUNDS'
    VARIABLES = 'VARIABLES'
    VAR_REGEXP = re.compile('[a-zA-Z_][a-zA-Z0-9_]*')
    COMP_REGEXP = re.compile('=|<=|<|>=|>')
    OP_REGEXP = re.compile('\+|-')
    COMMENT = '//'

    def __init__(self, linearProgram, fileName):
        self.linearProgram = linearProgram
        self.fileName = fileName

    @staticmethod
    def removeComment(string):
        return string.split('//')[0].strip()

    def fillVariables(self):
        inVar = False
        varIndex = 0
        lineno = 0
        with open(self.fileName) as f:
            for line in f:
                lineno+=1
                content = self.removeComment(line)
                if content == "":
                    continue
                elif not inVar and content == self.VARIABLES:
                    inVar = True
                elif inVar and content in [self.SUBJECT_TO, self.BOUNDS]+[x for x in self.OBJECTIVE]:
                    return
                elif inVar:
                    if(self.VAR_REGEXP.findall(content) != [content]):
                        raise Exception('Syntax error at line %s: %s is not a variable.' % (lineno, content))
                    self.linearProgram.indexFromVariable[content] = varIndex
                    self.linearProgram.variableFromIndex[varIndex] = content
                    varIndex += 1
        self.linearProgram.nbVariables = len(self.linearProgram.indexFromVariable)

    def parse(self):
        self.fillVariables()
