# Simplex

## Get started

```
pypy -OO -m main [-h] [-v] [-t] [-m MODE] inputfile
```

`-h` displays a short help and exit immediately.

`-v` displays the state of the system during the execution of the algorithm.

`-t` displays the time used to perform several steps of the program.

`-m MODE` choose the internal representation. `MODE` should be either `sparse` or `dense`.

`inputfile` is the file where is stored the linear program. Please have a look at
the provided examples to understand the syntax of those files.


## Data structure

The data structure is inspired from [Wikipedia](https://en.wikipedia.org/wiki/Simplex_algorithm).

Consider the following linear program:

```
MAXIMIZE
5x_1 + 4x_2 + 3x_3

SUBJECT TO
2x_1 + 3x_2 + x_3 <= 5
4x_1 + x_2 + 2x_3 <= 11
3x_1 + 4x_2 + 2x_3 <= 8

BOUNDS
x_1 >= 0
x_2 >= 0
x_3 >= 0

VARIABLES
x_1
x_2
x_3
```

It is represented as the following matrix:

| -5 | -4 | -3 |  0 |  0 |  0 |  0 |
|----|----|----|----|----|----|----|
|  2 |  3 |  1 |  1 |  0 |  0 |  5 |
|  4 |  1 |  2 |  0 |  1 |  0 | 11 |
|  3 |  4 |  2 |  0 |  0 |  1 |  8 |

In sparse mode, all the lines are represented as maps, without explicit representation
of the 0's. Thus, the above matrix would be stored as follows:

0→-5 | 1→-4 | 2→-3

0→2 | 1→3 | 2→1 | 3→1 | 6→5

0→4 | 1→1 | 2→2 | 4→1 | 6→11

0→3 | 1→4 | 2→2 | 5→1 | 6→8

It reduces significantly the number of operations to perform on some typical linear
programs, thus providing better performances.
