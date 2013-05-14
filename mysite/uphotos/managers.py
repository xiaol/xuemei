from django.db import models

class PhotoManager(models.Manager):
    """ Manager for the :class:`Photo` model.""" 
    def publish_photo(self, publisher, url, is_public, is_avatar, is_confirm):
	"""
	Publish a photo from a user.

	:param publisher:
	     The :class:`User` which publish the photo.

	:param is_public:
	     is public to view by other users.

	:param is_avatar:
	     is a avatar photo for user.

	"""
	photo = self.model(publisher=publisher,
			   image_url=url,
			   is_public=is_public,
			   is_avatar=is_avatar,
			   is_confirm=is_confirm)
	photo.save()
	
	return photo
