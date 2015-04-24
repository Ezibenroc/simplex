#!/usr/bin/env python3

import sys

def intToVar(n):
    return 'x_%d' % n

def generateLP(n):
    print('MAXIMIZE')
    print(' + '.join(intToVar(i) for i in range(n)))
    print('\nSUBJECT TO')
    for i in range(n-1):
        print('%s + %s <= 3' % (intToVar(i), intToVar(i+1)))
    print('\nBOUNDS')
    print('\n'.join('%s >= 1' % intToVar(i) for i in range(n)))
    print('\nVARIABLES')
    print('\n'.join(intToVar(i) for i in range(n)))

if __name__=='__main__':
    if len(sys.argv) != 2:
        sys.exit('Syntax: %s <number variables>' % sys.argv[0])
    generateLP(int(sys.argv[1]))
