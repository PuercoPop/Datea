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
