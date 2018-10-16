#!/usr/bin/env python

import mosquitto
from mqtt_settings import config
import datetime
import pytz
import numpy as np
import json


def on_message(mosq, obj, msg):
    print("%-20s %d %s" % (msg.topic, msg.qos, msg.payload))
    mosq.publish('pong', "Thanks", 0)


def on_publish(mosq, obj, mid):
    print("publish %s %s %s" % (mosq, obj, mid))


def main():
    cli = mosquitto.Mosquitto()
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
