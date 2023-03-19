from rest_framework import serializers
from main import models
from main.custom_models import good_models


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = good_models.Brand

        fields = ['id', 'name']
