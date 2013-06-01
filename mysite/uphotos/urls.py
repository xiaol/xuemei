from django.conf.urls.defaults import *
from uphotos import views as photos_views

urlpatterns = patterns('',
    url(r'^publish/$',
        photos_views.publish_photo,
        name='userena_umessages_compose'),
    url(r'^confirm-publish/(?P<photo_id>[^/]+)/$',
	photos_views.confirm_publish,name='uphotos_publish_confirm'),
    url(r'^(?P<photo_id>[\.\w-]+/toggle/$',
        photos_views.photo_toggle),
    url(r'^(?P<username>[\.\w-]+/',
	photos_views.PhotoListView.as_view()),
)
