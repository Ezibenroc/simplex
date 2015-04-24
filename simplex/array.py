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

    def __rmul__(self, other):
        return self.scalarOperation(other, lambda a, b: a*b)

    def __itruediv__(self, other):
        return self.inplaceScalarOperation(other, lambda a, b: a/b)

    def __truediv__(self, other):
        return self.scalarOperation(other, lambda a, b: a/b)

    def __div__(self, other):
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

class SparseLine(dict):
    def __init__(self, l=[]):
        for (i, x) in enumerate(l):
            if x != 0:
                self[i] = x
        self.__nbitem__ = len(l)

    def __getitem__(self, i):
        return self.get(i, 0)

    def __len__(self):
        return self.__nbitem__

    def __eq__(self, other):
        if isinstance(other, (dict, SparseLine)):
            return self.items() == other.items()
        else:
            return len(self) == len(other) and all(self[i] == other[i] for i in range(len(other)))

    def inplaceArrayOperation(self, other, f):
        for k in self.keys()|other.keys():
            elt = f(self[k], other[k])
            if elt:
                self[k] = elt
            else:
                self.pop(k, None)
        return self

    def arrayOperation(self, other, f):
        s = SparseLine()
        for k in self.keys()|other.keys():
            elt = f(self[k], other[k])
            if elt:
                s[k] = elt
        return s

    def inplaceScalarOperation(self, scalar, f):
        l = list(self.items())
        for k, elt in l:
            elt = f(self[k], scalar)
            if elt:
                self[k] = elt
            else:
                self.pop(k)
        return self

    def scalarOperation(self, scalar, f):
        s = SparseLine()
        for k in self.keys():
            elt = f(self[k], scalar)
            if elt:
                s[k] = elt
        return s

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

    def __rmul__(self, other):
        return self.scalarOperation(other, lambda a, b: a*b)

    def __itruediv__(self, other):
        return self.inplaceScalarOperation(other, lambda a, b: a/b)

    def __truediv__(self, other):
        return self.scalarOperation(other, lambda a, b: a/b)

    def __div__(self, other):
        return self.scalarOperation(other, lambda a, b: a/b)

    def addColumn(self, element, columnID):
        for k in sorted(self.keys(), key = lambda x:-x):
            if k < columnID:
                break
            self[k+1] = self[k]
            self.pop(k)
        self[columnID] = element

    def removeColumn(self, columnID):
        for k in sorted(self.keys()):
            if k < columnID:
                continue
            if k > columnID:
                self[k-1] = self[k]
            self.pop(k)

class SparseMatrix(list):
    def __init__(self, l):
        self.extend(SparseLine(elt) for elt in l)


    def addColumn(self, element, columnID=0):
        """
            Add a whole column made of the given element at the columnID position.
        """
        for l in self:
            l.addColumn(element, columnID) #[columnID:columnID] = [element]

    def removeColumn(self, columnID=0):
        """
            Remove the whole column.
        """
        for l in self:
            l.removeColumn(columnID)
