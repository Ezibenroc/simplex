class DenseMatrix(list):
    '''
        A class for dense matrix computations.
    '''
    def __init__(self, l):
        def a(x):
            if hasattr(x, '__iter__'):
                return DenseMatrix([a(y) for y in x])
            return x
        if hasattr(l, '__iter__'):
            self.extend(a(x) for x in l)
        else:
            self.append(l)

    def inplaceArrayOperation(self, other, f):
        '''
            Perform the operation self[i] = f(self[i], other[i]) for all indices i.
        '''
        assert(len(self)==len(other))
        for i in range(len(self)):
            self[i] = f(self[i], other[i])
        return self

    def arrayOperation(self, other, f):
        '''
            Return m such that m[i] = f(self[i], other[i]) for all indices i.
        '''
        assert(len(self)==len(other))
        return DenseMatrix(f(self[i], other[i]) for i in range(len(self)))

    def inplaceScalarOperation(self, scalar, f):
        '''
            Perform the operation self[i] = f(self[i], scalar) for all indices i.
        '''
        for i in range(len(self)):
            self[i] = f(self[i], scalar)
        return self

    def scalarOperation(self, scalar, f):
        '''
            Return m such that m[i] = f(self[i], scalar) for all indices i.
        '''
        return DenseMatrix(f(self[i], scalar) for i in range(len(self)))

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
        '''
            Add a whole column made of the given element at the columnID position.
        '''
        for l in self:
            l[columnID:columnID] = [element]

    def removeColumn(self, columnID=0):
        '''
            Remove the whole column.
        '''
        for l in self:
            del l[columnID]

    def argmin(self, inf=0, sup=None):
        '''
            Return the index of the minimum element.
        '''
        sup = sup if sup is not None else len(self)
        return (lambda array: min(zip(array, range(len(array))))[1])(self[inf:sup]) + inf

    def copy(self):
        return DenseMatrix(self)

class SparseLine(dict):
    '''
        A class for sparse line computations.
    '''
    def __init__(self, l=[]):
        if isinstance(l, dict):
            for k, elt in l.items():
                self[k] = elt
        else:
            for (i, x) in enumerate(l):
                if x != 0:
                    self[i] = x
        self.__nbitem__ = len(l)

    def __getitem__(self, i):
        if i<0:
            i=len(self)+i
        return self.get(i, 0)

    def __setitem__(self, i, elt):
        if i<0:
            i=len(self)+i
        if elt:
            super(self.__class__, self).__setitem__(i, elt)

    def __len__(self):
        return self.__nbitem__

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.items() == other.items()
        else:
            return len(self) == len(other) and all(self[i] == other[i] for i in range(len(other)))

    def __repr__(self):
        return ' | '.join(str(self[k]) for k in range(len(self)))

    def inplaceArrayOperation(self, other, f):
        '''
            Perform the operation self[i] = f(self[i], other[i]) for all indices i.
        '''
        for k in set(self.keys())|set(other.keys()):
            elt = f(self[k], other[k])
            if elt:
                self[k] = elt
            else:
                self.pop(k, None)
        return self

    def arrayOperation(self, other, f):
        '''
            Return m such that m[i] = f(self[i], other[i]) for all indices i.
        '''
        s = SparseLine()
        for k in set(self.keys())|set(other.keys()):
            elt = f(self[k], other[k])
            if elt:
                s[k] = elt
        return s

    def inplaceScalarOperation(self, scalar, f):
        '''
            Perform the operation self[i] = f(self[i], scalar) for all indices i.
        '''
        l = list(self.items())
        for k, elt in l:
            elt = f(self[k], scalar)
            if elt:
                self[k] = elt
            else:
                self.pop(k)
        return self

    def scalarOperation(self, scalar, f):
        '''
            Return m such that m[i] = f(self[i], scalar) for all indices i.
        '''
        s = SparseLine()
        for k in self.keys():
            s[k] = f(self[k], scalar)
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

    def addColumn(self, element, columnID=0):
        '''
            Add the given element at the columnID position.
        '''
        for k in sorted(self.keys(), key = lambda x:-x):
            if k < columnID:
                break
            self[k+1] = self[k]
            self.pop(k)
        self[columnID] = element
        self.__nbitem__ += 1

    def removeColumn(self, columnID=0):
        '''
            Remove the element laying at position columnID.
        '''
        for k in sorted(self.keys()):
            if k < columnID:
                continue
            if k > columnID:
                self[k-1] = self[k]
            self.pop(k)
        self.__nbitem__ -= 1

    def argmin(self, inf=0, sup=None):
        '''
            Return the index of the minimum element.
        '''
        sup = sup if sup is not None else len(self)
        if sup == -1:
            sup = len(self)-1
        if inf >= sup:
            raise Exception('inf is greater than sup, no argmin')
        m, minIndex = None, None
        keys = sorted(k for k in self.keys() if k >= inf and k < sup)
        if len(keys) == 0: # all elts are 0
            return 0
        elif keys[0] > inf:
            m, minIndex = 0, inf
        elif keys[-1] < sup-1:
            m, minIndex = 0, sup-1
        oldK = keys[0]-1
        for k in keys:
            if k-oldK > 1 and m > 0:
                m = 0
                minIndex = k
            else:
                if m is None or self[k] < m:
                    m = self[k]
                    minIndex = k
            oldK = k
        return minIndex if m is not None else inf # in case the min is 0

    def copy(self):
        return SparseLine(self)

class SparseMatrix(list):
    '''
        A class for sparse matrix computations.
    '''
    def __init__(self, l):
        self.extend(SparseLine(elt) for elt in l)


    def addColumn(self, element, columnID=0):
        '''
            Add a whole column made of the given element at the columnID position.
        '''
        for l in self:
            l.addColumn(element, columnID) #[columnID:columnID] = [element]

    def removeColumn(self, columnID=0):
        '''
            Remove the whole column.
        '''
        for l in self:
            l.removeColumn(columnID)

class Array(DenseMatrix):
    '''
        Inherits dynamically from one of the two classes DenseMatrix and SparseMatrix.
    '''
    pass
