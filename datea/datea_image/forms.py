from django import forms
from django.utils.translation import ugettext_lazy as _

# use a form mainly to validate incoming data 
class ImageUploadForm(forms.Form):
     
     image = forms.ImageField(label=_('Image'))
     object_type = forms.CharField(label=_('Object Type'), widget=forms.HiddenInput(), required=False)
     object_id = forms.CharField(label=_('Object ID'), widget=forms.HiddenInput(), required=False)
     object_field = forms.CharField(label=_('Object field'), widget=forms.HiddenInput(), required=False)
     thumb_preset = forms.CharField(label=_('Thumb preset'), widget=forms.HiddenInput(), required=False)
     