#!/usr/bin/env python3
import argparse
from simplex import LinearProgram, Parser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Simplex algorithm, to solve linear programs.')
    parser.add_argument('inputfile')
    parser.add_argument('-o', '--output', type=str,
            default='', help='Output file (default: standard output).')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Display informations during the solving of the program.')
    args = parser.parse_args()
    lp = LinearProgram()
    parser = Parser(lp, args.inputfile)
    parser.parse()
    lp.normalize()
    lp.solve()#args.verbose))
