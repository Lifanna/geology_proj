from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from main import models


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'


class LayerMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LayerMaterial
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    class Meta:
        model = models.CustomUser
        fields = ('id', 'first_name', 'last_name', 'role', 'username',)


class WaterCourseChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterCourse
        fields = '__all__'


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskStatus
        fields = '__all__'


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Line
        fields = '__all__'


class WaterCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterCourse
        fields = '__all__'


class WellSerializer(serializers.ModelSerializer):
    line = LineSerializer()

    class Meta:
        model = models.Well
        fields = '__all__'


class LicenseSerializer(serializers.ModelSerializer):
    geologist = CustomUserSerializer()
    mbu = CustomUserSerializer()
    pmbou = CustomUserSerializer()
    watercourses = WaterCourseSerializer(many=True)
    lines = LineSerializer(many=True)

    class Meta:
        model = models.License
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    line = LineSerializer()
    license = LicenseSerializer()
    wells = WellSerializer(many=True)
    responsible = CustomUserSerializer()
    status = TaskStatusSerializer()

    class Meta:
        model = models.Task
        fields = '__all__'


class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Layer
        fields = '__all__'
