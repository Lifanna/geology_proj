from django.contrib import admin
from django.contrib.admin import ModelAdmin
from main import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from main import forms


# @admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    """Регистрация модели CustomUser в админ панели"""

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'patronymic', 'team', 'phone_number', 'role')}),
        ('Permissions', {
            'fields': ('is_active',),
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )

    list_display = ('model_str', 'email')

    list_filter = ('email', 'first_name', 'last_name',)

    search_fields = ('email', 'first_name', 'last_name',)

    filter_horizontal = ()

    ordering = ('email',)

    add_fieldsets = (
        ("User Details", {'fields': ('username', 'email', 'password1', 'password2')}),
    )


admin.site.unregister(Group)
admin.site.register(models.CustomUser, CustomUserAdmin)


@admin.register(models.License)
class LicenseAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.LicenseStatus)
class LicenseStatusAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.WaterCourse)
class WaterCourseAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.Well)
class WellAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.Line)
class LineAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.TaskStatus)
class TaskStatusAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.Task)
class TaskAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.Team)
class TeamAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.Role)
class RoleAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.LineLicenseWaterCourse)
class LineLicenseWaterCourseAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.WellTask)
class WellTaskAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.Layer)
class LayerAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass


@admin.register(models.LayerMaterial)
class LayerMaterialAdmin(ModelAdmin):
    """Регистрация модели CustomUser в админ панели"""
    pass
