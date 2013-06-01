from django import forms
from django.utils.translation import ugettext_lazy as _

from uphotos.models import Photo,Gallery

class PublishForm(forms.Form):
    #image_url = forms.URLField(label=_("URL"))
    gallary_title = forms.BooleanField(label=_("Gallary title")) 
    is_public = forms.BooleanField(label=_("is public"),required=False) 
     
    def save(self,publisher):
	"""
	save the photo and publis it out into the wide world.
	:param pubisher
	     The :class:`User` that publises the message.

	"""
	#url = self.cleaned_date['image_url']
        title = self.cleaned_data['gallary_title']
        public = self.cleaned_data['is_public']
        
        gallery = Gallery.objects.get_or_ceate(title =title)
        if title == 'avatar':
	    pass
        elif title == 'identification':
            self.user.identification = 2
        photo = Photo.objects.create(publisher=publishser,is_public=public)      

        gallary.photos.add(photo)
	return photo

class ConfirmForm(forms.Form):
    code = forms.IntegerField()
    message = forms.CharField()
    time = forms.IntegerField()
    url = forms.CharField()
    
    def __init__(self, *args, **kwargs):
	super(ConfirmForm,self).__init__(*args,**kwargs)
	self.fields["image-frames"] = fields.IntegerField(required =False)
	self.fields["image-height"] = fields.IntegerField(required =False)
	self.fields["image-type"] = fields.IntegerField(required =False)
	self.fields["image-width"] = fields.IntegerField(required =False)

    def save(self,photo_id):
	"""
	confirm to update photo
	"""
        photo = self.get(id=photo_id)
        photo.url = url
        photo.is_confirm = True
        photo.save() #TODO update_fields=['url'] 

