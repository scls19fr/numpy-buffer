#!/usr/bin/env python
 
import mosquitto
import json
from mqtt_settings import config
from numpy_buffer import RingBuffer
import datetime
import pytz
import dateutil.parser

def on_message(mosq, obj, msg):
    data = json.loads(msg.payload.decode("utf-8")) # deserialization
    sent = dateutil.parser.parse(data['ts']) # iso 8601 to datetime.datetime
    data['ts'] = sent
    received = datetime.datetime.now(pytz.utc)
    lag = received - sent
    print("%-20s %d %s lag=%s" % (msg.topic, msg.qos, data, lag))
    #mosq.publish('pong', "Thanks", 0)
 
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
