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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.MainMenuView.as_view(), name="index"),
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

    # watercourses urls
    path('watercourses/add/<int:license_id>', views.WaterCourseCreateView.as_view(), name='watercourses_add'),
    path('watercourses/children/<int:pk>', api_views.WaterCourseChildrenDetailView.as_view(), name='watercourse_children'),
    path('objects/set_watercourses/<int:pk>', views.LicenseWaterCourseCreateView.as_view(), name='license_watercourse_add'),

    # watercourses urls
    # запилить CRUD для линий
    path('lines/add/<int:license_id>', views.LineCreateView.as_view(), name='lines_add'),
    path('objects/set_lines/<int:pk>', views.LineLicenseWaterCourseCreateView.as_view(), name='line_license_watercourse_add'),

    # wells urls
    path('wells/add/<int:task_id>', views.WellCreateView.as_view(), name='wells_add'),
    path('wells/<int:pk>', views.WellDetailView.as_view(), name='wells_detail'),
    path('wells/edit/<int:pk>', views.WellEditView.as_view(), name='wells_edit'),
    path('wells/set_welltasks/<int:pk>', views.WellTaskCreateView.as_view(), name='wells_task_add'),

    # layers urls
    path('layers/add', views.LayerCreateView.as_view(), name='layers_add'),
    path('layers/<int:pk>', views.LayerDetailView.as_view(), name='layers_detail'),
    path('layers/edit/<int:pk>', views.LayerUpdateView.as_view(), name='layers_edit'),

    # api urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/tasks/', api_views.TaskListView.as_view(), name='task_list'),
    path('api/layer/add', api_views.LayerCreateAPIView.as_view(), name='layer_add'),
    path('api/well/add', api_views.WellCreateAPIView.as_view(), name='well_add'),

    path('api/layer_materials/', api_views.LayerMaterialsListAPIView.as_view(), name='layer_materials_list'),
    path('api/synchronize/', api_views.SyncronizeViewSet.as_view({'post': 'create'}), name='synchronize'),

    # documentation urls
    path('documents/add', views.DocumentationCreateView.as_view(), name='layers_add'),
    path('documents/<int:pk>', views.DocumentationDetailView.as_view(), name='documentation_detail'),
    path('documents/edit/<int:pk>', views.DocumentationUpdateView.as_view(), name='documentation_edit'),

    path('mine/add', views.MineCreateView.as_view(), name='mine_edit'),
    path('mine/<int:pk>', views.MineDetailView.as_view(), name='mineetail'),
    path('mine/edit/<int:pk>', views.MineUpdateView.as_view(), name='mine_edit'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
