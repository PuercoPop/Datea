# -*- coding: utf-8 -*-
import os

from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from mptt.fields import TreeForeignKey
from sorl.thumbnail import get_thumbnail

from datea_image.models import DateaImage
from datea_category.models import DateaCategory


class SubclassingQuerySet(models.query.GeoQuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.as_leaf_class()
        else:
            return result

    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()


class DateaActionManager(models.GeoManager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)


class DateaAction(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'),
                             related_name="actions")

    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(
        _("Slug"), max_length=120,
        help_text=_("A string of text as a short id"
                    "for use at the url of this map"
                    " (alphanumeric and dashes only"))
    published = models.BooleanField(_("Published"), default=True,
                                    help_text=_("If checked, action becomes "
                                                "visible to others"))

    # timestamps
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    short_description = models.CharField(
        _("Short description / Slogan"), blank=True, null=True, max_length=140,
        help_text=_("A short description or slogan (max. 140 characters)."))
    hashtag = models.CharField(
        _("Hashtag"), blank=True, null=True, max_length=100,
        help_text=_("A twitter hashtag for your action"))
    category = TreeForeignKey(DateaCategory, verbose_name=_("Category"),
                              null=True, blank=True, default=None,
                              related_name="actions",
                              help_text=_("Choose a category for this action"))
    featured = models.BooleanField(_('Featured'), default=False)

    end_date = models.DateTimeField(
        _('End Date'), null=True, blank=True,
        help_text=_('Set an end date for your action (optional)'))

    image = models.ForeignKey(DateaImage, verbose_name=_('Image'), blank=True,
                              null=True, related_name="actions")

    action_type = models.CharField(_('Action type'), max_length=100,
                                   blank=True, null=True)

    # statistics
    item_count = models.PositiveIntegerField(_("Item count"), default=0)
    user_count = models.PositiveIntegerField(_("Participant count"), default=0)
    comment_count = models.PositiveIntegerField(_('Comment count'), default=0)
    follow_count = models.PositiveIntegerField(_('Follower count'), default=0)

    # generic relation to subclasses
    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    objects = DateaActionManager()

    # provide a way to know if published was changed
    def __init__(self, *args, **kwargs):
        super(DateaAction, self).__init__(*args, **kwargs)
        self.__orig_published = self.published

    def published_changed(self):
        return self.__orig_published != self.published

    def is_active(self):
        if not self.published:
            return False
        elif self.end_date and timezone.now() > self.end_date:
            return False
            return True

    def get_image_thumb(self, thumb_preset='action_image'):
        if self.image:
            return self.image.get_thumb(thumb_preset)
        else:
            Preset = settings.THUMBNAIL_PRESETS[thumb_preset]

            url = os.path.join(settings.MEDIA_ROOT,
                               'default/img/default-' + self.action_type +
                               '.png')
            #preserve format
            ext = url.split('.')[-1].upper()
            if ext not in ['PNG', 'JPG'] or ext == 'JPG':
                ext = 'JPEG'
                options = {'format': ext}
                if 'options' in Preset:
                    options.update(Preset['options'])
                    return get_thumbnail(url, Preset['size'], **options).url

    def get_absolute_url(self):
        return ugettext('/'+self.action_type+'/')+str(self.pk)

    def get_api_name(self, mode=None):
        return 'action'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(
                self.__class__)
            super(DateaAction, self).save(*args, **kwargs)

    def delete(self, using=None):
        if self.image:
            self.image.delete()
            super(DateaAction, self).delete(using=using)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == DateaAction):
            return self
            return model.objects.get(id=self.id)
