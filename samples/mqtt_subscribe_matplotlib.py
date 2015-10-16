#!/usr/bin/env python
 
import matplotlib.pyplot as plt
import mosquitto
import json
from mqtt_settings import config
from numpy_buffer import RingBuffer
import datetime
from timestamp import int2dt

maxlen = 500
data_x = RingBuffer(maxlen, datetime.datetime.utcnow(), dtype=datetime.datetime)
data_y = RingBuffer(maxlen)

fig, ax = plt.subplots()
line, = ax.plot(data_x.all[::-1], data_y.all[::-1], linestyle='-', marker='+', color='r', markeredgecolor='b')
ax.set_ylim([0, 100])

def on_message(mosq, obj, msg):
    data = json.loads(msg.payload.decode("utf-8")) # deserialization
    sent = int2dt(data['now']) # unix timestamp to datetime.datetime
    data['now'] = sent
    received = datetime.datetime.utcnow()
    lag = received - sent
    print("%-20s %d %s lag=%s" % (msg.topic, msg.qos, data, lag))
    #mosq.publish('pong', "Thanks", 0)

    data_x.append(sent)
    data_y.append(data['data']['y'])
    line.set_xdata(data_x.all[::-1])
    xmin, xmax = data_x.min(), data_x.max()
    if xmax > xmin:
        ax.set_xlim([xmin, xmax])
    line.set_ydata(data_y.all[::-1])
    ymin, ymax = data_y.min(), data_y.max()
    if ymax > ymin:
        ax.set_ylim([ymin, ymax])
    plt.pause(0.001)
 
def on_publish(mosq, obj, mid):
    pass

def main():
    cli = mosquitto.Mosquitto()
    cli.on_message = on_message
    cli.on_publish = on_publish

    #cli.tls_set('root.ca',
    #certfile='c1.crt',
    #keyfile='c1.key')

    #cli.username_pw_set("guigui", password="abloc")

    cli.connect(config['host'], config['port'], config['keepalive'])
    cli.subscribe("/sensors/#", 0)
 
    while cli.loop() == 0:
        pass

if __name__ == '__main__':
    main()
