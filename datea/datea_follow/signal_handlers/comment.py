from datea.datea_follow.models import DateaFollow, DateaHistory, DateaHistoryReceiver
from datea.datea_comment.models import DateaComment
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import post_save, pre_delete


#################################
# DATEA COMMENT SIGNALS
def on_comment_save(sender, instance, created, **kwargs):
    if instance is None: return
    
    ctype = ContentType.objects.get(model=instance.object_type.lower())
    receiver_obj = ctype.get_object_for_this_type(pk=instance.object_id)
    
    follow_key = ctype.model+'.'+str(receiver_obj.pk)
    history_key = follow_key+'_dateacomment.'+str(instance.pk)
    
    if created:
        # create notice on commented object
        hist_item = DateaHistory(
                        user=instance.user, 
                        acting_obj=instance,
                        follow_key = follow_key,
                        history_key = history_key,
                        sender_type = 'comment',
                        receiver_type = receiver_obj.get_api_name(mode='base')
                    )
        if hasattr(receiver_obj, 'action'):
            hist_item.action = receiver_obj.action
        
        hist_item.generate_extract('dateacomment', instance)    
        hist_item.save()
        
        # create receiver item
        recv_item = DateaHistoryReceiver(
            user = receiver_obj.user,
            name = receiver_obj.user.username,
            url = receiver_obj.get_absolute_url(),
            content_obj = receiver_obj,
            history_item = hist_item,
        )
        recv_item.save()
        
        hist_item.send_mail_to_receivers('comment')
        
        # create notice on the action, if relevant
        if hasattr(receiver_obj, 'action'):
            
            action = getattr(receiver_obj, 'action')
            action_follow_key = 'dateaaction.'+str(action.pk)
            
            # create notice on commented object's action
            action_hist_item = DateaHistory(
                        user=instance.user, 
                        acting_obj=instance,
                        follow_key = action_follow_key,
                        history_key = history_key,
                        sender_type = 'comment',
                        receiver_type = receiver_obj.get_api_name(mode='base'),
                        action = action
                    )
            action_hist_item.generate_extract('dateacomment', instance)
            action_hist_item.save()
            
            # generate receiver item
            action_recv_item = DateaHistoryReceiver(
                user = receiver_obj.user,
                name = receiver_obj.user.username,
                url = receiver_obj.get_absolute_url(),
                content_obj = receiver_obj,
                history_item = action_hist_item,
            )
            action_recv_item.save()
            
            if action.user != receiver_obj.user:
                action_hist_item.send_mail_to_action_owner('comment')
    else:
        hist_items = DateaHistory.objects.filter(history_key=history_key)
        for item in hist_items:
            item.generate_extract('dateacomment', instance)
            item.check_published()
            item.save()
        
        
              
def on_comment_delete(sender, instance, **kwargs):
    key =  instance.object_type.lower()+'.'+str(instance.object_id)+'_dateacomment.'+str(instance.pk)
    DateaHistory.objects.filter(history_key=key).delete()

def connect():
    post_save.connect(on_comment_save, sender=DateaComment)
    pre_delete.connect(on_comment_delete, sender=DateaComment)

