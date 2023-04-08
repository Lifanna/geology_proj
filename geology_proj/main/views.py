from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from main import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin


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


class MainMenuView(LoginRequiredMixin, ListView):
    template_name = "main/main_menu.html"
    queryset = models.Well

    def get_queryset(self):
        if self.request.GET.get("target") == "objects":
            queryset = models.License.objects.all()
        elif self.request.GET.get("target") == "users":
            queryset = models.CustomUser.objects.exclude(is_admin=True).all()
        elif self.request.GET.get("target") == "documents":
            queryset = models.Documentation.objects.all()
        elif self.request.GET.get("target") == "mine":
            queryset = models.Mine.objects.all()
        else:
            queryset = models.Task.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['target'] = self.request.GET.get('target')

        return context


"""OBJECTS CLASS-BASED VIEWS"""
class ObjectCreateView(CreateView):
    template_name = "main/objects/new.html"
    model = models.License
    form_class = forms.ObjectCreateForm
    success_url = "/main_menu?target=objects"
    # success_url = reverse_lazy("main_menu", kwargs={'target': 'objects'},)


class ObjectDetailView(DetailView):
    template_name = "main/objects/index.html"
    model = models.License
    queryset = models.License.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lines'] = models.LineLicenseWaterCourse.objects.filter(license=self.get_object()).all()
        context['watercourses'] = models.LicenseWaterCourse.objects.filter(license=self.get_object()).all()

        return context


class ObjectEditView(UpdateView):
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
class TaskCreateView(CreateView):
    template_name = "main/tasks/new.html"
    model = models.Task
    form_class = forms.TaskCreateForm
    success_url = "/main_menu?target=tasks"


class TaskDetailView(DetailView):
    template_name = "main/tasks/index.html"
    model = models.Task
    queryset = models.Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['wells'] = models.WellTask.objects.filter(task=self.get_object()).all()

        return context

class TaskEditView(UpdateView):
    template_name = "main/tasks/edit.html"
    model = models.Task
    form_class = forms.TaskUpdateForm
    success_url = "/main_menu?target=tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['wells'] = models.WellTask.objects.filter(task=self.get_object()).all()

        return context

    # def get_object(self, queryset):
    #     queryset = self.queryset
    #     return super().get_object(queryset)


"""USERS CLASS-BASED VIEWS"""
class CustomUserCreateView(CreateView):
    template_name = "main/users/new.html"
    model = models.CustomUser
    form_class = forms.CustomUserCreateForm
    success_url = "/main_menu?target=users"


class CustomUserDetailView(DetailView):
    template_name = "main/users/index.html"
    model = models.CustomUser
    queryset = models.CustomUser.objects.all()


class CustomUserEditView(UpdateView):
    template_name = "main/users/edit.html"
    model = models.CustomUser
    form_class = forms.CustomUserUpdateForm
    success_url = "/main_menu?target=users"

    # def get_object(self, queryset):
    #     queryset = self.queryset
    #     return super().get_object(queryset)


class CustomUserPasswordChangeView(UpdateView):
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
class WaterCourseCreateView(CreateView):
    template_name = "main/objects/watercourses/new.html"
    model = models.WaterCourse
    form_class = forms.WaterCourseCreateForm
    success_url = "/main_menu?target=objects"


class LicenseWaterCourseCreateView(CreateView):
    template_name = "main/objects/watercourses_licenses/new.html"
    model = models.WaterCourse
    form_class = forms.LicenseWaterCourseCreateForm
    # success_url = "/main_menu?target=users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_id = self.kwargs.get("pk")

        context['license_id'] = license_id
        context['license_name'] = models.License.objects.get(pk=license_id).name

        return context

    def get_success_url(self):
        success_url = f"/objects/edit/{self.kwargs.get('pk')}"

        return success_url


"""LINES CLASS-BASED VIEWS"""
class LineCreateView(CreateView):
    template_name = "main/objects/lines/new.html"
    model = models.Line
    form_class = forms.LineCreateForm
    success_url = "/main_menu?target=objects"


class LineLicenseWaterCourseCreateView(CreateView):
    template_name = "main/objects/lines_watercourses_licenses/new.html"
    model = models.LineLicenseWaterCourse
    form_class = forms.LineLicenseWaterCourseCreateForm
    # success_url = "/main_menu?target=users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_id = self.kwargs.get("pk")

        context['license_id'] = license_id
        context['license_name'] = models.License.objects.get(pk=license_id).name

        return context

    def get_success_url(self):
        success_url = f"/objects/edit/{self.kwargs.get('pk')}"

        return success_url


"""WELLS CLASS-BASED VIEWS"""
class WellCreateView(CreateView):
    template_name = "main/tasks/wells/new.html"
    model = models.Well
    form_class = forms.WellCreateForm
    success_url = "/main_menu?target=tasks"


class WellDetailView(DetailView):
    template_name = "main/tasks/wells/index.html"
    model = models.Well

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['layers'] = models.Layer.objects.filter(well=self.get_object()).all()

        return context


class WellEditView(UpdateView):
    template_name = "main/tasks/wells/edit.html"
    model = models.Well
    form_class = forms.WellUpdateForm

    def get_success_url(self):
        success_url = "/wells/edit/%s"%self.get_object().pk

        return success_url


class WellTaskCreateView(CreateView):
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
class LayerCreateView(CreateView):
    template_name = "main/tasks/wells/layers/new.html"
    model = models.Layer
    form_class = forms.LayerCreateForm

    def get_success_url(self):
        well_id = self.request.GET.get("well")
        return f"/wells/{well_id}"


class LayerDetailView(DetailView):
    template_name = "main/tasks/wells/layers/index.html"
    model = models.Layer
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        well_id = self.request.GET.get("well")
        context['back_url'] = f"/wells/{well_id}"
        context['well_id'] = well_id

        return context


class LayerUpdateView(UpdateView):
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
class DocumentationCreateView(CreateView):
    template_name = "main/documents/new.html"
    model = models.Documentation
    form_class = forms.DocumentsCreateForm
    success_url = "/main_menu?target=documents"


class DocumentationDetailView(DetailView):
    template_name = "main/documents/index.html"
    model = models.Documentation
    success_url = "/main_menu?target=documents"
    

class DocumentationUpdateView(UpdateView):
    template_name = "main/documents/edit.html"
    model = models.Documentation
    form_class = forms.DocumentsCreateForm
    success_url = "/main_menu?target=documents"


"""MINE CLASS-BASED VIEWS"""
class MineCreateView(CreateView):
    template_name = "main/mine/new.html"
    model = models.Mine
    form_class = forms.MineCreateForm
    success_url = "/main_menu?target=mine"


class MineDetailView(DetailView):
    template_name = "main/mine/index.html"
    model = models.Mine
    success_url = "/main_menu?target=mine"
    

class MineUpdateView(UpdateView):
    template_name = "main/mine/edit.html"
    model = models.Mine
    form_class = forms.MineCreateForm
    success_url = "/main_menu?target=mine"
