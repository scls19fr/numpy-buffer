#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from numpy_buffer import RingBuffer


def main():
    maxlen = 50
    # data_x = RingBuffer(maxlen)
    data_y = RingBuffer(maxlen)

    y = 100  # initial value

    fig, ax = plt.subplots()
    line, = ax.plot(data_y.all[::-1])
    delta_y = 20
    ax.set_ylim([y - delta_y, y + delta_y])

    while True:
        y = y + np.random.uniform(-1, 1)
        data_y.append(y)
        line.set_ydata(data_y.all[::-1])
        plt.pause(0.001)


if __name__ == '__main__':
    main()
