# Simplex


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
```

It is represented as the following matrix:

| -5 | -4 | -3 |  0 |  0 |  0 |  0 |
|----|----|----|----|----|----|----|
|  2 |  3 |  1 |  1 |  0 |  0 |  5 |
|  4 |  1 |  2 |  0 |  1 |  0 | 11 |
|  3 |  4 |  2 |  0 |  0 |  1 |  8 |
