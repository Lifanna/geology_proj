from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from main import models


# # Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.CustomUser
#         fields = '__all__'


class WaterCourseChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterCourse
        fields = '__all__'
