from django.conf.urls.defaults import *
from uphotos import views as photos_views

urlpatterns = patterns('',
    url(r'^publish/$',
        photos_views.publish_photo,
        name='userena_umessages_compose'),
)
