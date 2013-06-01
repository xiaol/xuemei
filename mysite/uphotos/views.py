# Create your views here.
from guardian.decorators import permission_required_or_403

import warnings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from userena.serializers import UserenaSerializer
from rest_framework.generics import ListAPIView
from uphotos.serializers import PhotoSerializer,PaginatedPhotoSerializer

import logging
logger = logging.getLogger(__name__)

from uphotos.forms import PublishForm,ConfirmForm
from follow.utils import follow as _follow, unfollow as _unfollow, toggle as _toggle
from mysite.forms import ToggleForm
from uphotos.models import Photo

@api_view(['POST'])
def publish_photo(request,publish_form=PublishForm):
    """
    publish a new photo
   
    :param publish_form:
	The form that is used for getting neccesary information.Defaults to :class:`PublishForm`.

    """

    initial_data = dict()

    form = publish_form(initial=initial_data)
    if request.method == "POST":
	form = publish_form(request.POST)
	if form.is_valid():
	    
	    photo = form.save(request.user)
	    return Response({'msg':'done'})
        
	else:
	    return Response(form.errors)

@api_view(['GET','POST'])
def confirm_publish(request,photo_id,confirm_form=ConfirmForm):
    if request.method == 'POST':
       form = confirm_form(request.POST)
       if form.is_valid():
          photo = form.save(photo_id)
          return Response({'msg':'Photo is confirmed'})

       else:
          logger.error("photo id:"+photo_id +" can't confirm")
          return Response({'msg':'negative'})
   
class PhotoListView(ListAPIView):
    serializer_class = PhotoSerializer
    paginate_by=12
    paginate_by_param = 'page_size'
    filter_fields = ('is_avatar',)

    def get_queryset(self):
        queryset = Photo.objects.all(publisher__username = self.username)
        return queryset

    def get(self,request, *args, **kwargs):
        self.username = kwargs['username']
        super(ListAPIView,self).get(self,request,*args,**kwargs)


@api_view(['POST'])
def photo_toggle(request,toggle_form=ToggleForm):
    """
    toggle to like or unlike photo
    """
    initial_data = dict()

    form = toggle_form(initial=intial_data)
    if request.method == "POST":
	form = toggle_form(request.POST)
        if form.is_Valid():
           cd = form.cleaned_data
           photo = Photo.objects.get(pk=cd['id'])
           _toggle(request.user,photo)
	else:
	   return Response(form.errors)
