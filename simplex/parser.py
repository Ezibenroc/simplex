from fractions import Fraction
import numpy
import re

class Parser:
    SPACES_REGEXP = re.compile('\s')
    OBJECTIVE = ['MINIMIZE', 'MAXIMIZE']
    SUBJECT_TO = 'SUBJECTTO'
    BOUNDS = 'BOUNDS'
    VARIABLES = 'VARIABLES'
    VAR = '[a-zA-Z][a-zA-Z0-9_]*'
    VAR_REGEXP = re.compile(VAR)
    NUMBER = '([\+-][ ]*)?(\d+/\d+|\d+)?'
    NUMBER_REGEXP = re.compile(NUMBER)
    LIT = '(%s)( )*%s' % (NUMBER, VAR)
    LIT_REGEXP = re.compile(LIT)
    LESS = '<='
    GREATER = '>='
    EQUAL = '='
    COMP_REGEXP = re.compile('%s|%s' % (LESS, GREATER))
    COMP_EQ_REGEXP = re.compile('%s|%s|%s' % (LESS, GREATER, EQUAL))
    COMMENT = '//'

    def __init__(self, simplex, fileName):
        self.simplex = simplex
        self.fileName = fileName

    @classmethod
    def removeComment(cls, string):
        return cls.SPACES_REGEXP.sub('', string.split('//')[0])

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
                self.simplex.nbVariables += 1
                self.simplex.indexFromVariable[content] = varIndex
                self.simplex.variableFromIndex[varIndex] = content
                varIndex += 1
            elif mode == self.SUBJECT_TO:
                comp = self.COMP_REGEXP.findall(content)
                if len(comp) > 0:
                    self.simplex.nbConstraints += len(comp)
                else:
                    if len(re.findall(self.EQUAL, content)) != 1:
                        raise Exception('Syntax error at line %s: %s is not a valid comparison.' % (lineno, content))
                    else:
                        self.simplex.nbConstraints += 2 # equality translated into two inequalities
            elif mode == self.BOUNDS:
                raise Exception('BOUNDS not yet implemented.')
            elif mode in self.OBJECTIVE:
                continue
            else:
                raise Exception('Syntax error at line %s.' % lineno)
        self.simplex.tableaux = numpy.array([[Fraction(0, 1)]*(self.simplex.nbVariables + self.simplex.nbConstraints + 1)\
            for i in range(self.simplex.nbConstraints + 1)])
        self.simplex.basicVariables += list(range(self.simplex.nbVariables, self.simplex.nbVariables+self.simplex.nbConstraints))
        for v in range(self.simplex.nbVariables, self.simplex.nbVariables + self.simplex.nbConstraints):
            self.simplex.variableFromIndex[v] = '_slack_%d' % (v-self.simplex.nbVariables)
            self.simplex.indexFromVariable['_slack_%d' % (v-self.simplex.nbVariables)] = v

    def newExpression(self, lineno, constraintID, content, objective):
        op = self.COMP_EQ_REGEXP.findall(content)
        content = self.COMP_EQ_REGEXP.split(content)
        if objective and len(op) != 0:
            raise Exception('Syntax error at line %s: comparison operator not allowed in objective.' % lineno)
        elif not objective and len(op) != 1:
            raise Exception('Syntax error at line %s: one and only one comparison operator is allowed in constraints.' % lineno)
        if len(op) == 1 :
            bound = content[1].strip()
            bound_match = self.NUMBER_REGEXP.match(bound)
            if not bound_match or bound_match.end() != len(bound):
                raise Exception('Syntax error at line %s: invalid bound.' % lineno)
            bound = Fraction(bound)
            self.simplex.tableaux[constraintID, self.simplex.nbVariables+constraintID-1] = 1
            if op[0] == self.LESS:
                self.simplex.tableaux[constraintID][-1] = bound
            elif op[0] == self.GREATER:
                self.simplex.tableaux[constraintID][-1] = -bound
            else: # self.EQUAL
                self.simplex.tableaux[constraintID+1, self.simplex.nbVariables+constraintID] = 1
                self.simplex.tableaux[constraintID][-1] = bound
                self.simplex.tableaux[constraintID+1, -1] = -bound
        expression = content[0]
        if expression == "":
            raise Exception('Syntax error at line %s: empty expression.' % lineno)
        while expression != "":
            literalMatch = self.LIT_REGEXP.match(expression)
            if not literalMatch:
                raise Exception('Syntax error at line %s: invalid sub-expression: %s.' % (lineno, expression))
            literal = expression[literalMatch.start():literalMatch.end()]
            expression = expression[literalMatch.end():].strip()
            number_match = self.NUMBER_REGEXP.match(literal)
            number_string = literal[number_match.start():number_match.end()]
            if number_string in {'+', ''}:
                number = Fraction(1)
            elif number_string == '-':
                number = Fraction(-1)
            else:
                number = Fraction(number_string)
            variable = literal[number_match.end():].strip()
            try:
                variable = self.simplex.indexFromVariable[variable]
            except KeyError:
                raise Exception('Syntax error at line %s: unknown variable: %s.' % (lineno, variable))
            if len(op) == 0 or op[0] == self.GREATER:
                self.simplex.tableaux[constraintID][variable] = -number
            elif op[0] == self.LESS:
                self.simplex.tableaux[constraintID][variable] = number
            else: # self.EQUAL
                self.simplex.tableaux[constraintID][variable] = number
                self.simplex.tableaux[constraintID+1, variable] = -number
        return constraintID+2 if op == [self.EQUAL] else constraintID+1

    def fillTableaux(self):
        mode = None
        constraintID = 0
        for (lineno, content) in self.lineRange():
            if content in [self.VARIABLES, self.SUBJECT_TO, self.BOUNDS]+[x for x in self.OBJECTIVE]:
                mode = content
            elif mode == self.VARIABLES: # variables handled in fillVariables
                continue
            elif mode in self.OBJECTIVE:
                self.simplex.objective = mode
                constraintID = self.newExpression(lineno, constraintID, content, True)
                mode = None
            elif mode == self.SUBJECT_TO:
                constraintID = self.newExpression(lineno, constraintID, content, False)
            else:
                raise Exception('Syntax error at line %s.' % lineno)

    def parse(self):
        self.fillVariables()
        self.fillTableaux()
