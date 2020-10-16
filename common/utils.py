import functools
from datetime import datetime
import random
import string
import time

from dateutil import *
from flask import request, make_response

import helper as _helper

_config = _helper.get_config()

# _storage_config = _config['storage']
# _encrypt_key = _config['novel']['encrypt_key'].encode('utf-8')

_local_zone = tz.tzlocal()


def get_local_now():
    return datetime.now().replace(tzinfo=_local_zone)


def get_default_tz():
    return _local_zone


def radom_name(length=8):
    return ''.join(random.choices(string.ascii_uppercase, k=length))


def now_ts_ms():
    return int(round(time.time() * 1000))
