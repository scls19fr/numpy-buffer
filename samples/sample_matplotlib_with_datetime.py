#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import datetime
from numpy_buffer import RingBuffer


def main():
    maxlen = 500
    data_x = RingBuffer(maxlen, datetime.datetime.utcnow(), dtype=datetime.datetime)
    data_y = RingBuffer(maxlen)

    y = 100  # initial value

    fig, ax = plt.subplots()
    line, = ax.plot(data_x.all[::-1], data_y.all[::-1], linestyle='-', marker='+', color='r', markeredgecolor='b')
    delta_y = 20
    ax.set_ylim([y - delta_y, y + delta_y])

    while True:
        x = datetime.datetime.utcnow()
        y = y + np.random.uniform(-1, 1)
        data_x.append(x)
        data_y.append(y)
        line.set_xdata(data_x.all[::-1])
        xmin, xmax = data_x.min(), data_x.max()
        if xmax > xmin:
            ax.set_xlim([xmin, xmax])
        line.set_ydata(data_y.all[::-1])
        ymin, ymax = data_y.min(), data_y.max()
        if ymax > ymin:
            ax.set_ylim([ymin, ymax])
        plt.pause(0.001)


if __name__ == '__main__':
    main()
