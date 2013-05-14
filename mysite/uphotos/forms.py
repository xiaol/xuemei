from django import forms
from django.utils.translation import ugettext_lazy as _

class PublishForm(forms.Form):
    image_url = forms.URLField(label=_("URL"))
    is_confirm = forms.BooleanField(label=_("Confirm")) 
    
    def save(self,publisher):
	"""
	save the photo and publis it out into the wide world.

	:param pubisher
	     The :class:`User` that publises the message.

	:param image_url:
	     image url to upyun storage.

	:param is_confirm:
	     image is confirm to upload to upyun.

	"""
	url = self.cleaned_date['image_url']
	corfirm = self.cleaned_data['is_confirm']

        photo = Photo.objects.publish_photo(publisher,
				   	    url,
					    corfirm)

	return photo
