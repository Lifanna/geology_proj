"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# -*- coding: utf-8 -*-
from django.urls import path
from . import views
from main.api import api_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),
    path('main_menu/', views.MainMenuView.as_view(), name="main_menu"),
    
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('registration/', views.CustomRegistrationView.as_view(), name='registration'),

    # objects urls
    path('objects/add', views.ObjectCreateView.as_view(), name='objects_add'),
    path('objects/<int:pk>', views.ObjectDetailView.as_view(), name='objects_detail'),
    path('objects/edit/<int:pk>', views.ObjectEditView.as_view(), name='objects_edit'),

    # tasks urls
    path('tasks/add', views.TaskCreateView.as_view(), name='tasks_add'),
    path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='tasks_detail'),
    path('tasks/edit/<int:pk>', views.TaskEditView.as_view(), name='tasks_edit'),

    # users urls
    path('users/add', views.CustomUserCreateView.as_view(), name='users_add'),
    path('users/<int:pk>', views.CustomUserDetailView.as_view(), name='users_detail'),
    path('users/edit/<int:pk>', views.CustomUserEditView.as_view(), name='users_edit'),
    path('users/edit/password/<int:pk>', views.CustomUserPasswordChangeView.as_view(), name='users_change_password'),

    path('watercourses/add', views.WaterCourseCreateView.as_view(), name='watercourse_add'),
    path('watercourses/children/<int:pk>', api_views.WaterCourseChildrenDetailView.as_view(), name='watercourse_children'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
