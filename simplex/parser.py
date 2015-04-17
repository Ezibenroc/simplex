from fractions import Fraction
from .linearProgram import Literal, Expression, LinearProgram
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
    LIT = '(?P<factor>%s)( )*(?P<variable>%s)' % (NUMBER, VAR)
    LIT_REGEXP = re.compile(LIT)
    LESS = '<='
    GREATER = '>='
    EQUAL = '='
    COMP_REGEXP = re.compile('%s|%s' % (LESS, GREATER))
    EQ_REGEXP = re.compile('%s' % EQUAL)
    COMP_EQ_REGEXP = re.compile('%s|%s|%s' % (LESS, GREATER, EQUAL))
    COMMENT = '//'

    def __init__(self, linearProgram, fileName):
        self.linearProgram = linearProgram
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
    @staticmethod
    def stringToNumber(n):
        if n in {'+', ''}:
            return Fraction(1)
        elif n == '-':
            return Fraction(-1)
        else:
            return Fraction(n)

    @classmethod
    def stringToNumberCheck(cls, n, lineno):
        m = cls.NUMBER_REGEXP.match(n)
        if m is None or m.end() != len(n):
            raise Exception('Syntax error at line %s.' % lineno)
        return cls.stringToNumber(n)

    @classmethod
    def parseLiteralList(cls, line, lineno=None):
        old = None
        litList = []
        for lit in cls.LIT_REGEXP.finditer(line):
            if old is None:
                if lit.start() != 0:
                    raise Exception('Syntax error at line %s.' % lineno)
            else:
                if lit.start() != old:
                    raise Exception('Syntax error at line %s.' % lineno)
            old = lit.end()
            litList.append(Literal(
                cls.stringToNumber(lit.group('factor')),
                lit.group('variable')
            ))
        if old != len(line):
            raise Exception('Syntax error at line %s.' % lineno)
        return litList

    @classmethod
    def parseLine(cls, line, lineno=None):
        expr = Expression()
        compList = list(cls.COMP_REGEXP.finditer(line))
        start, end = 0, len(line)
        if len(compList) > 2:
            raise Exception('Syntax error at line %s.' % lineno)
        elif len(compList) == 2:
            start = compList[0].end()
            end = compList[1].start()
            if compList[0].group() != compList[1].group():
                raise Exception('Syntax error at line %s.' % lineno)
            else:
                if compList[0].group() == cls.LESS:
                    expr.leftBound = cls.stringToNumberCheck(line[:compList[0].start()], lineno)
                    expr.rightBound = cls.stringToNumberCheck(line[compList[1].end():], lineno)
                else:
                    expr.rightBound = cls.stringToNumberCheck(line[:compList[0].start()], lineno)
                    expr.leftBound = cls.stringToNumberCheck(line[compList[1].end():], lineno)
        elif len(compList) == 1:
            end = compList[0].start()
            if compList[0].group() == cls.LESS:
                expr.rightBound = cls.stringToNumberCheck(line[compList[0].end():], lineno)
            else:
                expr.leftBound = cls.stringToNumberCheck(line[compList[0].end():], lineno)
        else:
            eqList = list(cls.EQ_REGEXP.finditer(line))
            if len(eqList) > 1:
                raise Exception('Syntax error at line %s.' % lineno)
            elif len(eqList) == 1:
                end = eqList[0].start()
                expr.rightBound = cls.stringToNumberCheck(line[eqList[0].end():], lineno)
                expr.leftBound = expr.rightBound
        expr.literalList = cls.parseLiteralList(line[start:end], lineno)
        return expr

    def parse(self):
        mode = None
        for (lineno, content) in self.lineRange():
            if content in [self.VARIABLES, self.SUBJECT_TO, self.BOUNDS]+[x for x in self.OBJECTIVE]:
                mode = content
            else:
                expr = self.parseLine(content, lineno)
                if mode == self.VARIABLES:
                    if ((expr.leftBound, expr.rightBound) != (None, None) or
                            len(expr.literalList) != 1 or
                            expr.literalList[0].factor != 1):
                        raise Exception('Syntax error at line %s.' % lineno)
                    else:
                        self.linearProgram.variables.append(expr.literalList[0].variable)
                elif mode in self.OBJECTIVE:
                    if (expr.leftBound, expr.rightBound) != (None, None) or len(expr.literalList) == 0:
                        raise Exception('Syntax error at line %s.' % lineno)
                    self.linearProgram.objective = mode
                    self.linearProgram.objectiveFunction = (expr, lineno)
                    mode = None
                elif mode == self.SUBJECT_TO:
                    if (expr.leftBound, expr.rightBound) == (None, None) or len(expr.literalList) == 0:
                        raise Exception('Syntax error at line %s.' % lineno)
                    self.linearProgram.subjectTo.append((expr, lineno))
                else:
                    if (expr.leftBound, expr.rightBound) == (None, None) or len(expr.literalList) != 1 or expr.literalList[0].factor != 1:
                        raise Exception('Syntax error at line %s.' % lineno)
                    self.linearProgram.bounds.append((expr, lineno))
        self.linearProgram.check()
