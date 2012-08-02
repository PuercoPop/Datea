from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from datea.datea_follow.models import DateaFollow, DateaHistory, DateaHistoryReceiver, DateaNotifySettings
from api_base import DateaBaseResource, ApiKeyPlusWebAuthentication, DateaBaseAuthorization


class FollowResource(DateaBaseResource):
    
    #user = fields.ToOneField('datea.datea_api.profile.UserResource', 
    #        attribute='user', full=False, readonly=True)
    
    def hydrate(self,bundle):
        if bundle.request.method == 'POST':
            bundle.obj.user = bundle.request.user  
        return bundle
     
    class Meta:
        queryset = DateaFollow.objects.all()
        resource_name = 'follow'
        allowed_methods = ['get', 'post', 'delete']
        filtering={
                'id' : ['exact'],
                'user': ALL_WITH_RELATIONS,
                'object_type': ['exact'],
                'object_id': ['exact'],
                'follow_key': ['exact']
                }
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
        limit = 50
        
        
class HistoryResource(DateaBaseResource):
    
    receiver_items = fields.ToManyField('datea.datea_api.follow.HistoryReceiverResource', 
            attribute="receiver_items",related_name='receiver_items', full=True, readonly=True)
    
    def dehydrate(self, bundle):
        bundle.data['username'] = bundle.obj.user.username
        bundle.data['user_url'] = bundle.obj.user.profile.get_absolute_url()
        return bundle
    
    class Meta:
        queryset= DateaHistory.objects.all()
        resource_name= 'history'
        allowed_methods = ['get']
        excludes = ['receiver_id', 'acting_id']
        filtering = {
                     'id': ['exact'],
                     'user': ALL_WITH_RELATIONS,
                     'action': ALL_WITH_RELATIONS,
                     'follow_key': ['exact','in'],
                     'history_key': ['exact'],
                     'history_type': ['exact'],
                     'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
                     }
        limit = 20
        
        
class HistoryReceiverResource(DateaBaseResource):
    
    def dehydrate(self, bundle):
        del bundle.data['resource_uri']
        return bundle
    
    class Meta:
        queryset = DateaHistoryReceiver.objects.filter(published=True)
        allowed_methods = ['get']
        fields = ['name', 'url']
        

class NotifySettingsResource(DateaBaseResource):
    
    def hydrate(self,bundle):
        if bundle.request.method == 'PUT':
            #preserve original owner
            orig_object = DateaNotifySettings.objects.get(pk=bundle.data['id'])
            bundle.obj.user = orig_object.user
            print vars(bundle.obj)
            
        return bundle
    
    class Meta:
        queryset = DateaNotifySettings.objects.all()
        resource_name = 'notify_settings'
        allowed_methods = ['get', 'put']
        filtering = {
                     'user': ALL_WITH_RELATIONS,
                     }
        limit = 1
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
    
        