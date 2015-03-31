#!/usr/bin/env python3

from simplex import LinearProgram, Parser

if __name__ == '__main__':
    lp = LinearProgram()
    parser = Parser(lp, 'example2.in')
    parser.parse()
    print(lp.solve(True))
