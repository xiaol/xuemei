from django import forms
from django.utils.translation import ugettext_lazy as _

class PublishForm(forms.Form):
    image_url = forms.URLField(label=_("URL"))
    is_confirm = forms.BooleanField(label=_("Confirm")) 
    is_avatar = forms.BooleanField(label=_("Avatar")) 
    is_public = forms.BooleanField(label=_("Public"),default=True) 
     
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
        avatar = self.cleaned_data['is_avatar']
        public = self.cleaned_data['is_public']

        photo = self.model(publisher=publisher,
                           image_url=url,
                           is_public=public,
                           is_avatar=avatar,
                           is_confirm=corfirm)
        photo.save() 					    

	return photo
