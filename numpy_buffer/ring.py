#!/usr/bin/env python

import numpy as np

class RingBuffer(object):
    def __init__(self, size_max, default_value=0.0, dtype=float, overflow=None):
        """initialization"""
        self.clear(size_max, default_value, dtype, overflow)

    def clear(self, size_max=None, default_value=None, dtype=None, overflow=None):
        """clear ring"""
        if size_max is not None:
            self.size_max = size_max

        if default_value is not None:
            self.default_value = default_value

        if dtype is not None:
            self.dtype = dtype

        if overflow is not None:
            self.overflow = overflow

        if not isinstance(default_value, np.ndarray):
            self._data = np.empty(size_max, dtype=dtype)
            self._data.fill(default_value)
        else:
            if len(default_value) == size_max:
                self._data = default_value
            else:
                raise(NotImplementedError("len(default_value)=%d but size_max=%d",
                    " but they should be equal" % (len(default_value), size_max)))

        self.size = 0
        
        self.full = False
        self.append = self._append_not_full        

    def _append_not_full(self, value):
        """append an element"""
        self._data = np.roll(self._data, 1)
        self._data[0] = value 

        self.size += 1
                
        if self.size == self.size_max:
            self.full  = True
            self.append = self._append_full
            self.overflow = self.overflow(self)

    def _append_full(self, value):
        """append an element when buffer is full"""
        self._data = np.roll(self._data, 1)
        self._data[0] = value


    @property
    def all(self):
        """return a list of elements from the oldest to the newest (len: size_max)"""
        return self._data
        
    @property
    def partial(self):
        """return a list of elements from the oldest to the newest (len: size)"""
        return self.all[0:self.size]

    def view(self, *args, **kwargs):
        return self.partial[::-1].view(*args, **kwargs)
    
    def __len__(self):
        """return size (not size_max)"""
        return self.size

    def __getitem__(self, key):
        """get element"""
        return self._data[key]

    def __repr__(self):
        """return string representation"""
        s = """<%s
    all:     %s
    partial: %s
    size/size_max: %d / %d
>""" % (self.__class__.__name__, 
    self.all.__repr__(), 
    self.partial.__repr__(),
    self.size, self.size_max
)
        return s

    def overflow(self, *args, **kwargs):
        return

    def min(self, all=False):
        """return min"""
        if all:
            return self.all.min()
        else:
            return self.partial.min()

    def max(self, all=True):
        """return max"""
        if all:
            return self.all.max()
        else:
            return self.partial.max()
