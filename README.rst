|Build Status|

Numpy Buffer
============

A `Python <https://www.python.org/>`_ `NumPy <http://www.numpy.org/>`_ implementation of buffer.

Ring Buffer
-----------

Description
^^^^^^^^^^^

See `description of a ring buffer (or circular buffer) <https://en.wikipedia.org/wiki/Circular_buffer>`_.

Usage
^^^^^

.. code:: python

    In [1]: from numpy_buffer import RingBuffer

    In [2]: N = 10

    In [3]: ring = RingBuffer(size_max=10, default_value=0.0, dtype=float)

    In [4]: ring
    Out[4]:
    <RingBuffer
        all:     array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])
        partial: array([], dtype=float64)
        size/size_max: 0 / 10
    >

    In [5]: ring.append(1.2)

    In [6]: ring
    Out[6]:
    <RingBuffer
        all:     array([ 1.2 ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.])
        partial: array([ 1.2])
        size/size_max: 1 / 10
    >

    In [7]: ring.append(2.1)

    In [8]: ring
    Out[8]:
    <RingBuffer
        all:     array([ 2.1 ,  1.2 ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.,  0.])
        partial: array([ 2.1 ,  1.2])
        size/size_max: 2 / 10
    >

    In [9]: ring.all
    Out[9]: array([ 2.1,  1.2,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ])

    In [10]: ring.partial
    Out[10]: array([ 2.1,  1.2])

    In [11]: ring.partial[::-1]
    Out[11]: array([ 1.2,  2.1])

Install
-------

.. code:: bash

    pip install numpy_buffer


.. |Build Status| image:: https://travis-ci.org/scls19fr/numpy_buffer.svg?branch=master
   :target: https://travis-ci.org/scls19fr/numpy_buffer