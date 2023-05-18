from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from main import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from main.services import export_to_excel_service
import os
from uuid import uuid4
from django.core.files.base import ContentFile


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name='account/login.html'

    def get_success_url(self):
        return reverse_lazy('main_menu')
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class CustomRegistrationView(CreateView):
    template_name = "account/registration.html"
    model = models.CustomUser
    form_class = forms.CustomUserRegistrationForm


from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('main.add_license')
def the_view(request):
    print(request.user.has_perm('main.add_license'))
        
    for per in request.user.get_user_permissions():
        print("ASDASD", per)
    return render(request, 'main/index.html')

class MainMenuView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'main.add_license'
    template_name = "main/main_menu.html"
    queryset = models.Well

    def get_queryset(self):
        user = self.request.user.get_all_permissions()
        # print("DDDDDD: ", user)
        # print(self.request.user.has_perm('main.add_license'))
        if self.request.user.has_perm('main.add_license'):
            print("DA")
        else:
            print("NET")
        if self.request.GET.get("target") == "objects":
            queryset = models.License.objects.all()

            if self.request.GET.get('order'):
                ordering = self.request.GET.get('order')
                queryset = models.License.objects.order_by(ordering).all()
        elif self.request.GET.get("target") == "users":
            queryset = models.CustomUser.objects.exclude(is_admin=True).all()
        elif self.request.GET.get("target") == "documents":
            queryset = models.Documentation.objects.order_by('-id').all()
        elif self.request.GET.get("target") == "mine":
            queryset = models.Mine.objects.all()
        else:
            queryset = models.Task.objects.all()

            if self.request.GET.get('order'):
                ordering = self.request.GET.get('order')
                queryset = models.Task.objects.order_by(ordering).all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['target'] = self.request.GET.get('target')

        return context


"""OBJECTS CLASS-BASED VIEWS"""
class ObjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('main.add_license',)
    template_name = "main/objects/new.html"
    model = models.License
    form_class = forms.ObjectCreateForm
    success_url = "/main_menu?target=objects"
    # success_url = reverse_lazy("main_menu", kwargs={'target': 'objects'},)


class ObjectDetailView(LoginRequiredMixin, DetailView):
    template_name = "main/objects/index.html"
    model = models.License
    queryset = models.License.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lines'] = models.LineLicenseWaterCourse.objects.filter(license=self.get_object()).all()
        context['watercourses'] = models.LicenseWaterCourse.objects.filter(license=self.get_object()).all()

        return context


class ObjectEditView(LoginRequiredMixin, UpdateView):
    template_name = "main/objects/edit.html"
    model = models.License
    form_class = forms.ObjectUpdateForm
    success_url = "/main_menu?target=objects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formm'] = forms.LicenseWaterCourseCreateForm
        
        context['lines'] = models.LineLicenseWaterCourse.objects.filter(license=self.get_object()).all()
        context['watercourses'] = models.LicenseWaterCourse.objects.filter(license=self.get_object()).all()

        return context

    # def get_object(self, queryset):
    #     queryset = self.queryset
    #     return super().get_object(queryset)


"""TASKS CLASS-BASED VIEWS"""
class TaskCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/tasks/new.html"
    model = models.Task
    form_class = forms.TaskCreateForm
    success_url = "/main_menu?target=tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    template_name = "main/tasks/index.html"
    model = models.Task
    queryset = models.Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['wells'] = models.WellTask.objects.filter(task=self.get_object()).all()
        context['images'] = models.TaskImage.objects.filter(task=self.get_object()).all()

        return context

class TaskEditView(LoginRequiredMixin, UpdateView):
    template_name = "main/tasks/edit.html"
    model = models.Task
    form_class = forms.TaskUpdateForm
    success_url = "/main_menu?target=tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['wells'] = models.WellTask.objects.filter(task=self.get_object()).all()
        context['images'] = models.TaskImage.objects.filter(task=self.get_object()).all()

        return context


class TaskImageRemoveView(LoginRequiredMixin, DeleteView):
    template_name = "main/tasks/task_images/remove.html"
    model = models.TaskImageSingle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = models.Task.objects.get(pk=self.kwargs.get('task_id'))

        return context

    def get_success_url(self):
        success_url = f"/tasks/edit/{self.kwargs.get('task_id')}"

        return success_url


"""USERS CLASS-BASED VIEWS"""
class CustomUserCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/users/new.html"
    model = models.CustomUser
    form_class = forms.CustomUserCreateForm
    success_url = "/main_menu?target=users"


class CustomUserDetailView(LoginRequiredMixin, DetailView):
    template_name = "main/users/index.html"
    model = models.CustomUser
    queryset = models.CustomUser.objects.all()


class CustomUserEditView(LoginRequiredMixin, UpdateView):
    template_name = "main/users/edit.html"
    model = models.CustomUser
    form_class = forms.CustomUserUpdateForm
    success_url = "/main_menu?target=users"

    # def get_object(self, queryset):
    #     queryset = self.queryset
    #     return super().get_object(queryset)


class CustomUserPasswordChangeView(LoginRequiredMixin, UpdateView):
    template_name = "main/users/change_password.html"
    model = models.CustomUser
    form_class = forms.CustomUserPasswordChangeForm

    def get_success_url(self):
        success_url = "/users/edit/%s"%self.get_object().pk

        return success_url

    def get_form(self, *args, **kwargs):
        form = super(CustomUserPasswordChangeView, self).get_form(*args, **kwargs)
        form.fields['password'].required = False

        return form


"""WATERCOURSES CLASS-BASED VIEWS"""
class WaterCourseCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/objects/watercourses/new.html"
    model = models.WaterCourse
    form_class = forms.WaterCourseCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_id = self.kwargs.get("license_id")

        context['license_id'] = license_id

        return context

    def get_success_url(self):
        success_url = f"/objects/edit/{self.kwargs.get('license_id')}"

        return success_url


class LicenseWaterCourseCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/objects/watercourses_licenses/new.html"
    model = models.WaterCourse
    form_class = forms.LicenseWaterCourseCreateForm
    # success_url = "/main_menu?target=users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_id = self.kwargs.get("pk")

        context['license_id'] = license_id
        context['license_name'] = models.License.objects.get(pk=license_id).short_name

        return context

    def get_success_url(self):
        success_url = f"/objects/edit/{self.kwargs.get('pk')}"

        return success_url


class LicenseWaterCourseRemoveListView(LoginRequiredMixin, ListView):
    template_name = "main/objects/watercourses_licenses/remove.html"
    model = models.LicenseWaterCourse
    # success_url = "/main_menu?target=users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_id = self.kwargs.get("pk")

        context['license_id'] = license_id
        context['license_name'] = models.License.objects.get(pk=license_id).short_name
        context['object_list'] = models.LicenseWaterCourse.objects.filter(license=self.kwargs.get("pk"))

        return context

    def get_success_url(self):
        success_url = f"/objects/edit/{self.kwargs.get('pk')}"

        return success_url


class LicenseWaterCourseRemoveView(LoginRequiredMixin, DeleteView):
    template_name = "main/objects/watercourses_licenses/remove.html"
    model = models.LicenseWaterCourse

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_id = self.kwargs.get("pk")

        context['license_id'] = license_id
        context['license_name'] = models.License.objects.get(pk=license_id).short_name
        context['object_list'] = models.LicenseWaterCourse.objects.filter(license=self.kwargs.get("pk"))

        return context

    def get_success_url(self):
        success_url = f"/objects/edit/{self.kwargs.get('license_id')}"

        return success_url


"""LINES CLASS-BASED VIEWS"""
class LineCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/objects/lines/new.html"
    model = models.Line
    form_class = forms.LineCreateForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_id = self.kwargs.get("license_id")

        context['license_id'] = license_id

        return context

    def get_success_url(self):
        success_url = f"/objects/edit/{self.kwargs.get('license_id')}"

        return success_url


class LineLicenseWaterCourseCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/objects/lines_watercourses_licenses/new.html"
    model = models.LineLicenseWaterCourse
    form_class = forms.LineLicenseWaterCourseCreateForm
    # success_url = "/main_menu?target=users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_id = self.kwargs.get("pk")

        context['license_id'] = license_id
        context['license_name'] = models.License.objects.get(pk=license_id).short_name

        return context

    def get_success_url(self):
        success_url = f"/objects/edit/{self.kwargs.get('pk')}"

        return success_url


class LineLicenseWaterCourseRemoveListView(LoginRequiredMixin, ListView):
    template_name = "main/objects/lines_watercourses_licenses/remove.html"
    model = models.LineLicenseWaterCourse
    form_class = forms.LineLicenseWaterCourseCreateForm
    # success_url = "/main_menu?target=users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_id = self.kwargs.get("pk")

        context['license_id'] = license_id
        context['license_name'] = models.License.objects.get(pk=license_id).short_name
        context['object_list'] = models.LineLicenseWaterCourse.objects.filter(license=self.kwargs.get("pk"))

        return context

    def get_success_url(self):
        success_url = f"/objects/edit/{self.kwargs.get('pk')}"

        return success_url


class LineLicenseWaterCourseRemoveView(LoginRequiredMixin, DeleteView):
    template_name = "main/objects/lines_watercourses_licenses/remove.html"
    model = models.LineLicenseWaterCourse

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_id = self.kwargs.get("pk")

        context['license_id'] = license_id
        context['license_name'] = models.License.objects.get(pk=license_id).short_name

        return context

    def get_success_url(self):
        success_url = f"/objects/edit/{self.kwargs.get('license_id')}"

        return success_url


"""WELLS CLASS-BASED VIEWS"""
class WellCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/tasks/wells/new.html"
    model = models.Well
    form_class = forms.WellCreateForm
    success_url = "/main_menu?target=tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_id = self.kwargs.get("license_id")

        context['license_id'] = license_id

        return context

    def get_success_url(self):
        license_id = self.kwargs.get("license_id")
        success_url = f"/objects/set_watercourses/{license_id}"

        return success_url


class WellDetailView(LoginRequiredMixin, DetailView):
    template_name = "main/tasks/wells/index.html"
    model = models.Well

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['task_id'] = self.kwargs.get("task_id")
        context['layers'] = models.Layer.objects.filter(well=self.get_object()).all()

        return context


class WellEditView(LoginRequiredMixin, UpdateView):
    template_name = "main/tasks/wells/edit.html"
    model = models.Well
    form_class = forms.WellUpdateForm

    def get_success_url(self):
        success_url = "/wells/edit/%s"%self.get_object().pk

        return success_url


class WellTaskCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/tasks/wells/well_tasks/new.html"
    model = models.WellTask
    form_class = forms.WellTaskCreateForm
    success_url = "/main_menu?target=tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        task_id = self.kwargs.get("pk")

        context['task_id'] = task_id
        context['task_name'] = models.License.objects.get(pk=task_id).short_name

        return context


"""LAYERS CLASS-BASED VIEWS"""
class LayerCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/tasks/wells/layers/new.html"
    model = models.Layer
    form_class = forms.LayerCreateForm

    def get_success_url(self):
        well_id = self.request.GET.get("well")
        return f"/wells/{well_id}"


class LayerDetailView(LoginRequiredMixin, DetailView):
    template_name = "main/tasks/wells/layers/index.html"
    model = models.Layer
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        well_id = self.request.GET.get("well")
        context['back_url'] = f"/wells/{well_id}"
        context['well_id'] = well_id

        return context


class LayerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "main/tasks/wells/layers/edit.html"
    model = models.Layer
    form_class = forms.LayerCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        well_id = self.request.GET.get("well")
        context['back_url'] = f"/wells/{well_id}"

        return context

    def get_success_url(self):
        well_id = self.request.GET.get("well")
        return f"/wells/{well_id}"


"""DOCUMENTATION CLASS-BASED VIEWS"""
class DocumentationCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/documents/new.html"
    model = models.Documentation
    form_class = forms.DocumentsCreateForm
    success_url = "/main_menu?target=documents"

    def form_valid(self, form):
        license = form.cleaned_data.get('license')
        watercourse = form.cleaned_data.get('watercourse')
        line = form.cleaned_data.get('line')
        well = form.cleaned_data.get('well')

        print(license.watercourses.all())

        watercourse_bound = models.LicenseWaterCourse.objects.get(watercourse = watercourse)

        export_service = export_to_excel_service.ExportToExcelService()
        export_service.build_document(license=license, watercourse=watercourse, watercourse_bound=watercourse_bound, line=line, well=well)

        return super().form_valid(form)

    def get_success_url(self):
        url = f'/documents/{self.object.id}'

        return url


class DocumentationDetailView(LoginRequiredMixin, DetailView):
    template_name = "main/documents/index.html"
    model = models.Documentation
    success_url = "/main_menu?target=documents"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file'] = '/media/example.xlsx'

        return context


class DocumentationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "main/documents/edit.html"
    model = models.Documentation
    form_class = forms.DocumentsCreateForm
    success_url = "/main_menu?target=documents"


"""MINE CLASS-BASED VIEWS"""
class MineCreateView(LoginRequiredMixin, CreateView):
    template_name = "main/mine/new.html"
    model = models.Mine
    form_class = forms.MineCreateForm
    success_url = "/main_menu?target=mine"


class MineDetailView(LoginRequiredMixin, DetailView):
    template_name = "main/mine/index.html"
    model = models.Mine
    success_url = "/main_menu?target=mine"


class MineUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "main/mine/edit.html"
    model = models.Mine
    form_class = forms.MineCreateForm
    success_url = "/main_menu?target=mine"


# class MineImageCreateView(CreateView):
    