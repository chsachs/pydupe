from collections import deque
from collections.abc import MutableSet
from typing import Tuple


class LuTable(MutableSet):
    """
    class used to represent an Lookup Table for File Hashes. This is basically a Dictionary with hashvalue as key and a list of files as values.
    A LuTable is therefore an intermediate between a Mapping and a Set. The set is implemented as list and not as set() objects for performance reasons:
    A set is faster for searching and membership testing, but has a high memory overhead. In contrast lists have low memory overhead but slower membership testing.
    However, the list of files is typically in the order of 10th, therefore memory impact was rated more severe. To speedup adding of elements,
    the list is implemented as collections.deque objects. See for further reference:
    https://docs.python.org/3/library/collections.abc.html
    https://code.activestate.com/recipes/576694/

    A mapping to the hashes is supplied together with set operations for the values. 

    """
    def __init__(self, iterable=None) -> None:
        self._hashlu = {}
        if iterable is not None:
            self |= iterable

    def __contains__(self, x: Tuple) -> bool:
        if x[0] in self._hashlu:
            return (x[1] in self._hashlu[x[0]])
        else:
            return False

    def __iter__(self):
        for hash in self._hashlu.keys():
            for file in self._hashlu[hash]:
                yield hash, file

    def __len__(self) -> int:
        return sum([len(x) for x in self._hashlu.values()])

    def add(self, item: Tuple) -> None:
        if item[0] not in self._hashlu:
            self._hashlu[item[0]] = deque()
        self._hashlu[item[0]].append(item[1])

    def discard(self, x: Tuple) -> None:
        self._hashlu[x[0]].remove(x[1])
        if self._hashlu[x[0]] == deque([]):
            self._hashlu.pop(x[0])

    def __str__(self):
        return(str(self._hashlu))

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def lor(self, other):
        for k, v in iter(other):
            if k in self._hashlu.keys():
                if v not in self._hashlu[k]:
                    self._hashlu[k].append(v)

    def ldel(self, iterable=None):
        if iterable is not None:
            for k in iterable:
                if k in self._hashlu:
                    del self._hashlu[k]

    def keys(self):
        return self._hashlu.keys()

    def values(self):
        return self._hashlu.values()

    def lextend(self, other, key):
        if key not in self._hashlu:
            self._hashlu[key] = deque()
        self._hashlu[key].extend(other[key])

    def __getitem__(self, key):
        return self._hashlu[key]

    def __setitem__(self, key, value):
        """
        be careful with value:
        deque('test')" == ddeque(['t', 'e', 's', 't'])
        deque(['test]) == deque(['test'])
        """
        if key not in self._hashlu.keys():
            self._hashlu[key] = deque()
        self._hashlu[key] = deque(value)

    def __delitem__(self, key):
        del self._hashlu[key]

    def as_dict_of_lists_of_str(self):
        dict_of_lists = {}
        for hash in self._hashlu:
            for value in self._hashlu[hash]:
                if hash not in dict_of_lists:
                    dict_of_lists[hash] = []
                dict_of_lists[hash].append(str(value))
        return dict_of_lists

# %%
