# -*- coding: utf-8 -*-

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'datea',
        'USER': 'PuercoPop',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

OPENGRAPH_DEFAULT_IMAGE = ''
FACEBOOK_APP_ID = ''

BLOG_FEED_URL = ''
BLOG_FEED_CACHE_TIMEOUT = ''
BLOG_NAME = ''
BLOG_URL = ''
