#!/usr/bin/env python

from numpy_buffer import RingBuffer
import numpy as np

def test_ring():
    N = 10
    def print_overflow(*args, **kwargs):
        print("OVERFLOW of %s" % args[0])
        #raise NotImplementedError
    ring = RingBuffer(size_max=N, default_value=0.0, dtype=float, overflow=print_overflow)
    for i in range(1, N + 5):
        ring.append(i)
        assert ring[0] == i
        if i < N:
            assert not ring.full
        else:
            assert ring.full

    assert isinstance(ring.all, np.ndarray)
    assert isinstance(ring.partial, np.ndarray)

def test_min_max():
    N = 5
    ring = RingBuffer(size_max=N, default_value=-1)
    ring.append(2)
    ring.append(1)
    ring.append(4)
    ring.append(3)
    assert ring.min() == 1
    assert ring.min(all=True) == -1
    assert ring.max() == 4