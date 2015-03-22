from fractions import Fraction
import numpy
import re

class Parser:
    OBJECTIVE = ['MINIMIZE', 'MAXIMIZE']
    SUBJECT_TO = 'SUBJECT TO'
    BOUNDS = 'BOUNDS'
    VARIABLES = 'VARIABLES'
    VAR = '[a-zA-Z_][a-zA-Z0-9_]*'
    VAR_REGEXP = re.compile(VAR)
    NUMBER = '\d+/\d+|\d+'
    OP = '\+|-'
    LIT = '(%s)?( )*(%s)?( )*%s' % (OP, NUMBER, VAR)
    COMP_REGEXP = re.compile('<=|>=|>|<')
    COMMENT = '//'

    def __init__(self, linearProgram, fileName):
        self.linearProgram = linearProgram
        self.fileName = fileName

    @staticmethod
    def removeComment(string):
        return string.split('//')[0].strip()

    def lineRange(self):
        lineno = 0
        with open(self.fileName) as f:
            for line in f:
                lineno+=1
                content = self.removeComment(line)
                if content != "":
                    yield (lineno, content)

    def fillVariables(self):
        varIndex = 0
        mode = None
        for (lineno, content) in self.lineRange():
            if content in [self.VARIABLES, self.SUBJECT_TO, self.BOUNDS]+[x for x in self.OBJECTIVE]:
                mode = content
            elif mode == self.VARIABLES: # variables handled in fillVariables
                if(self.VAR_REGEXP.findall(content) != [content]):
                    raise Exception('Syntax error at line %s: %s is not a variable.' % (lineno, content))
                self.linearProgram.nbVariables += 1
                self.linearProgram.indexFromVariable[content] = varIndex
                self.linearProgram.variableFromIndex[varIndex] = content
                varIndex += 1
            elif mode in {self.BOUNDS, self.SUBJECT_TO}:
                comp = self.COMP_REGEXP.findall(content)
                if len(comp) > 0:
                    self.linearProgram.nbConstraints += len(comp)
                else:
                    if len(re.findall('=', content)) != 1:
                        raise Exception('Syntax error at line %s: %s is not a valid comparison.' % (lineno, content))
                    else:
                        self.linearProgram.nbConstraints += 2 # equality translated into two inequalities
        self.linearProgram.tableaux = numpy.zeros((self.linearProgram.nbConstraints + 1, self.linearProgram.nbVariables + self.linearProgram.nbConstraints + 1))

    def parse(self):
        self.fillVariables()
