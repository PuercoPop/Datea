# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    "datea_action.views",
    url("^actions/(?P<path>[a-z0-9-/]+)", 'redirect_to_hash_en'),
    url("^acciones/(?P<path>[a-z0-9-/]+)", 'redirect_to_hash_es'),
)
