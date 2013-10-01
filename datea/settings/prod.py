# -*- coding: utf-8 -*-
from os import getenv


SECRET_KEY = getenv('DATEA_SK')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
