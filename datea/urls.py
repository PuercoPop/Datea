from django.conf import settings
from django.conf.urls import patterns, include, url
from tastypie.api import Api


from django.contrib import admin
admin.autodiscover()

#API resources
from datea_api.auth import Accounts
from datea_api.profile import ProfileResource,UserResource
from datea_api.mapping import MappingResource,MapItemResource
from datea_api.category import FreeCategoryResource
from datea_api.vote import VoteResource
from datea_api.image import ImageResource
from datea_api.action import ActionResource
from datea_api.contenttypes import ContentTypeResource

v1_api = Api(api_name='v1')
v1_api.register(Accounts())
v1_api.register(ProfileResource())
v1_api.register(UserResource())
v1_api.register(MappingResource())
v1_api.register(MapItemResource())
v1_api.register(FreeCategoryResource())
v1_api.register(VoteResource())
v1_api.register(ImageResource())
v1_api.register(ActionResource())
v1_api.register(ContentTypeResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'datea.datea_home.views.home', name='home'),
    # url(r'^datea/', include('datea.foo.urls')),
    
    url(r'^api/',include(v1_api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'', include('social_auth.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
    
) + urlpatterns
