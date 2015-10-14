#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some function to manage datetime / timedelta
as integer (unix timestamp)

Usage:

from timestamp import *
"""

import datetime
import pytz

UNIX_EPOCH_naive = datetime.datetime(1970, 1, 1, 0, 0) #offset-naive datetime
UNIX_EPOCH_offset_aware = datetime.datetime(1970, 1, 1, 0, 0, tzinfo = pytz.utc) #offset-aware datetime
UNIX_EPOCH = UNIX_EPOCH_naive

TS_MULT_us = 1e6

def now_timestamp(ts_mult=TS_MULT_us, epoch=UNIX_EPOCH):
    return(int((datetime.datetime.utcnow() - epoch).total_seconds()*ts_mult))

def int2dt(ts, ts_mult=TS_MULT_us):
    """Returns datetime from timestamp (integer)"""
    return(datetime.datetime.utcfromtimestamp(float(ts)/ts_mult))

def dt2int(dt, ts_mult=TS_MULT_us, epoch=UNIX_EPOCH):
    """Returns integer from timedelta"""
    delta = dt - epoch
    return(int(delta.total_seconds()*ts_mult))

def td2int(td, ts_mult=TS_MULT_us):
    """Returns integer from datetime"""
    return(int(td.total_seconds()*ts_mult))

def int2td(ts, ts_mult=TS_MULT_us):
    """Returns timedelta from timestamp (integer)"""
    return(datetime.timedelta(seconds=float(ts)/ts_mult))

def int_from_last_candle(dt, td):
    """Returns integer from datetime and timedelta"""
    return(dt2int(dt) - dt2int(dt) % td2int(td))

#def int_to_next_candle(dt, td):
#    return(dt2int(dt) + dt2int(dt) % td2int(td))

def ts_candle_from_ts(ts, timeframe_int):
    """Return candle timestamp from a timestamp and a given timeframe (integer)"""
    return((ts // timeframe_int) * timeframe_int)
