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


## About performances

The following commands performs a profiling of the program on the file `examples/generated_100.in`.

In dense mode:

```bash
python -m cProfile -s cumtime main.py -m dense examples/generated_100.in
```

In sparse mode:

```bash
python -m cProfile -s cumtime main.py -m sparse examples/generated_100.in
```

It takes a total of 7.452 seconds to run the program on this example in sparse mode.
In dense mode, it takes 44.198 seconds. Thus, the sparse representation is a huge
improvement in some typical examples where there are a lot of 0's in the matrix.

Let us focus on the sparse representation.

We notice that there is a huge bottleneck: 7.214 seconds are spent in the function
`performPivot` (file `simplex.py`). This represents 97% of the total time.

A deeper analysis (by putting timers in the program) tells us that a great part of this
time is spent on the following line of this function:
```python
self.tableaux[r] -= coeff*self.tableaux[row]
```

Indeed, this operation is applied on all lines of the matrix for each pivot.

We tried to improve the performances by replacing this operation by a single function
performing the substraction and the multiplication, instead of the two functions.
Unfortunately, it increased the execution time.

More research are needed to tackle this problem. A solution could be to code this
part of the program in C++.
