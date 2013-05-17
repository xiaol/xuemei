from rest_framework import serializers, pagination
from profiles.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
     class Meta:
        model = Profile
        fields = ('gender',)

class PaginatedProfileSerializer(pagination.PaginationSerializer):
     """
     Serializes page objects of user querysets
     """
     class Meta:
         object_serializer_class = ProfileSerializer
