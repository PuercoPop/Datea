# -*- coding: utf-8 -*-
from os import getenv


SECRET_KEY = getenv('DATEA_SK')
TWITTER_CONSUMER_KEY = getenv('TWITTER_CK')
TWITTER_CONSUMER_SECRET = getenv('TWITTER_CS')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
