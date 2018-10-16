#!/usr/bin/env python

import paho.mqtt.client as mqtt
from mqtt_settings import config
import datetime
import pytz
import numpy as np
import json


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print("%-20s %d %s" % (msg.topic, msg.qos, msg.payload))
    client.publish('pong', "Thanks", 0)


def on_publish(client, userdata, msg):
    print("publish %s %s %s" % (client, userdata, msg))


def main():
    cli = mqtt.Client()
    cli.on_connect = on_connect
    cli.on_message = on_message
    cli.on_publish = on_publish

    # cli.tls_set('root.ca',
    # certfile='c1.crt',
    # keyfile='c1.key')

    # cli.username_pw_set("guigui", password="abloc")

    cli.connect(config['host'], config['port'], config['keepalive'])

    y = 100  # initial value

    while cli.loop() == 0:
        now = datetime.datetime.now(pytz.utc)
        y = y + np.random.uniform(-1, 1)
        data = {
            'ts': now.isoformat(),
            'd': {
                'y': y
            }
        }
        payload = json.dumps(data)  # serialization
        cli.publish(topic='/sensors/sensor01', payload=payload, qos=0, retain=False)


if __name__ == '__main__':
    main()
