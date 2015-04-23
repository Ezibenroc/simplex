#!/usr/bin/env python3
import argparse
from simplex import LinearProgram, Parser
import time
import sys

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
    parser.add_argument('-t', '--timer', action='store_true',
            help='Display the time needed to complete each task.')
    args = parser.parse_args()
    lp = LinearProgram()
    parser = Parser(lp, args.inputfile)
    clock = Clock()
    parser.parse()
    clock.tic('Parsing')
    lp.normalize()
    clock.tic('Normalization')
    lp.solve(args.verbose)
    clock.tic('Resolution')
    if args.timer:
        print("\n%s" % clock)
