from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from main import models, forms


# Create your views here.
def index(request):
    return render(request, "main/index.html")


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name='account/login.html'

    def get_success_url(self):
        return reverse_lazy('main_menu')
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class CustomRegistrationView(CreateView):
    template_name = "account/registration.html"
    model = models.CustomUser
    form_class = forms.CustomUserRegistrationForm


class MainMenuView(ListView):
    template_name = "main/main_menu.html"
    queryset = models.Well

    def get_queryset(self):
        if self.request.GET.get("target") == "objects":
            queryset = models.License.objects.all()
        elif self.request.GET.get("target") == "users":
            queryset = models.CustomUser.objects.exclude(is_admin=True).all()
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


class ObjectEditView(UpdateView):
    template_name = "main/objects/edit.html"
    model = models.License
    form_class = forms.ObjectUpdateForm
    success_url = "/main_menu?target=objects"

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


class TaskEditView(UpdateView):
    template_name = "main/tasks/edit.html"
    model = models.Task
    form_class = forms.TaskUpdateForm
    success_url = "/main_menu?target=tasks"

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
    success_url = "/main_menu?target=users"
