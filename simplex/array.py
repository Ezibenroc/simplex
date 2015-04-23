class Array(list):

    def __init__(self, l):
        def a(x):
            if hasattr(x, '__iter__'):
                return Array([a(y) for y in x])
            return x
        if hasattr(l, '__iter__'):
            self.extend(a(x) for x in l)
        else:
            self.append(l)

    def inplaceArrayOperation(self, other, f):
        assert(len(self)==len(other))
        for i in range(len(self)):
            self[i] = f(self[i], other[i])
        return self

    def arrayOperation(self, other, f):
        assert(len(self)==len(other))
        return Array(f(self[i], other[i]) for i in range(len(self)))

    def inplaceScalarOperation(self, scalar, f):
        for i in range(len(self)):
            self[i] = f(self[i], scalar)
        return self

    def scalarOperation(self, scalar, f):
        return Array(f(self[i], scalar) for i in range(len(self)))

    def __iadd__(self, other):
        return self.inplaceArrayOperation(other, lambda a, b: a+b)

    def __add__(self, other):
        return self.arrayOperation(other, lambda a, b: a+b)

    def __isub__(self, other):
        return self.inplaceArrayOperation(other, lambda a, b: a-b)

    def __sub__(self, other):
        return self.arrayOperation(other, lambda a, b: a-b)

    def __imul__(self, other):
        return self.inplaceScalarOperation(other, lambda a, b: a*b)

    def __mul__(self, other):
        return self.scalarOperation(other, lambda a, b: a*b)

    def __itruediv__(self, other):
        return self.inplaceScalarOperation(other, lambda a, b: a/b)

    def __truediv__(self, other):
        return self.scalarOperation(other, lambda a, b: a/b)

    def addColumn(self, element, columnID=0):
        """
            Add a whole column made of the given element at the columnID position.
        """
        for l in self:
            l[columnID:columnID] = [element]

    def removeColumn(self, columnID=0):
        """
            Remove the whole column.
        """
        for l in self:
            del l[columnID]
