from follow.utils import follow as _follow, unfollow as _unfollow, toggle as _toggle

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from userena.serializers import UserenaSerializer

import logging
logger = logging.getLogger(__name__)

from mysite.forms import ToggleForm
from uphotos.models import Photo
from django.contrib.auth.models import User

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

@api_view(['POST'])
def user_toggle(request,toggle_form=ToggleForm):
    """
    toggle to follow or unfollow user
    """ 
    initial_data = dict()

    form = toggle_form(initial=intial_data)
    if request.method == "POST":
        form = toggle_form(request.POST)
        if form.is_Valid():
           cd = form.cleaned_data
           user = User.objects.get(pk=cd['id'])
           _toggle(request.user,user)
        else:
           return Response(form.errors)

