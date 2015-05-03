#!/usr/bin/env python3
import argparse
from simplex import LinearProgram, Parser, Array, SparseMatrix, DenseMatrix
import time
import sys

LATEX_HEADER = r'''
\documentclass[a4paper,11pt]{report}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage[T1]{fontenc}
\usepackage[left=1.5cm, right=2cm, top=3cm, bottom=2cm]{geometry}
\usepackage{amsmath,amsthm,amssymb,array,enumerate,cancel,nth,stmaryrd,fancyhdr,calc,mathtools}
\parindent=0mm
\begin{document}

'''

LATEX_FOOTER = r'''
\end{document}
'''

class bcolors:
    """
        From http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Clock:
    '''
        A class to measure the time spent in some parts of the program.
    '''
    def __init__(self):
        self.time = time.time()
        self.start = self.time
        self.allTimes = []

    def tic(self, string):
        assert not string in self.allTimes
        toc = time.time()
        self.allTimes.append((string, toc-self.time))
        self.time = toc

    def __str__(self):
        length = max(len('Total'), max(len(x[0]) for x in self.allTimes)) + 1
        toc = time.time()
        string = bcolors.BOLD + bcolors.OKGREEN
        for s, t in self.allTimes:
            string+= s.ljust(length) + ('%.4fs\n' % t)
        return string + 'Total'.ljust(length) + ('%.4fs\n' % (toc-self.start)) + bcolors.ENDC

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Simplex algorithm, to solve linear programs.')
    parser.add_argument('inputfile')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Display informations during the solving of the program.')
    parser.add_argument('-l', '--latex', type=str,
            default=None, help='Store informations of the solution in the given file.')
    parser.add_argument('-t', '--timer', action='store_true',
            help='Display the time needed to complete each task.')
    parser.add_argument('-m', '--mode', type=str,
            default='sparse', help='Internal representation (sparse/dense, default=sparse).')
    args = parser.parse_args()
    if args.mode == 'sparse':
        Array.__bases__ = (SparseMatrix,)
    elif args.mode == 'dense':
        Array.__bases__ = (DenseMatrix,)
    else:
        sys.exit('Unknown mode: %s.' % args.mode)
    # Instanciation of the linear program
    lp = LinearProgram()
    # Instanciation of the parser
    parser = Parser(lp, args.inputfile)
    clock = Clock()
    # Parsing
    parser.parse()
    clock.tic('Parsing')
    # Normalization
    lp.normalize()
    clock.tic('Normalization')
    # Resolution
    if args.latex:
        latex = open(args.latex, 'w')
        latex.write(LATEX_HEADER)
    else:
        latex = None
    lp.solve(args.verbose, latex)
    if latex:
        latex.write(LATEX_FOOTER)
        latex.close()
    clock.tic('Resolution')
    if args.timer:
        print("\n%s" % clock)
