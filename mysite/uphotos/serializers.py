from rest_framework import serializers, pagination
from uphotos.models import Photo

class PhotoSerializer(serializers.ModelSerializer):
     class Meta:
        model = Photo
        fields = ('image_url',)

class PaginatedPhotoSerializer(pagination.PaginationSerializer):
     class Meta:
        object_serializer_class = PhotoSerializer
