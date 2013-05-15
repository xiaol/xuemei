# Create your views here.
from guardian.decorators import permission_required_or_403

import warnings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from userena.serializers import UserenaSerializer

import logging
logger = logging.getLogger(__name__)

from uphotos.forms import PublishForm

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

@api_view(['POST']
def like_or_not(request,status=status):
    """
    like or not like a photo

    :param status:
	status indicate the boolean status.
    """
    pass
