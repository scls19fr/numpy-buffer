#!/usr/bin/env python

import paho.mqtt.client as mqtt
import json
from mqtt_settings import config
import datetime
import pytz
import dateutil.parser


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/sensors/#", 0)


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode("utf-8"))  # deserialization
    sent = dateutil.parser.parse(data['ts'])  # iso 8601 to datetime.datetime
    data['ts'] = sent
    received = datetime.datetime.now(pytz.utc)
    lag = received - sent
    print("%-20s %d %s lag=%s" % (msg.topic, msg.qos, data, lag))
    # mosq.publish('pong', "Thanks", 0)


def on_publish(client, userdata, msg):
    pass


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

    cli.loop_forever()


if __name__ == '__main__':
    main()
