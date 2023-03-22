from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from main import models
from django.contrib.auth.password_validation import validate_password


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = '__all__'


"""OBJECTS FORMS"""
class ObjectCreateForm(forms.ModelForm):
    class Meta:
        model = models.License
        fields = '__all__'


class ObjectUpdateForm(forms.ModelForm):
    class Meta:
        model = models.License
        fields = (
            'short_name',
            'name',
            'geologist',
            'status',
            'used_enginery',
            'mbu',
            'pmbou',
            'primary_watercourse',
            'secondary_watercourse',
            'comment',
        )


"""TASKS FORMS"""
class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = (
            'short_name',
            'description',
            'license',
            'line',
            'well',
            'responsible',
            'status',
            'comment',
        )


"""USERS FORMS"""
class CustomUserCreateForm(UserCreationForm):

    class Meta:
        model = models.CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'patronymic',
            'team',
            'phone_number',
            'email',
            'role',
        )


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'patronymic',
            'team',
            'phone_number',
            'email',
            'role',
        )


class CustomUserPasswordChangeForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput())

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError({"password1": "Пароли должны совпадать!"})

        return super().clean()

    def save(self, commit=False):
        id = self.cleaned_data['id']
        password1 = self.cleaned_data['password1']

        models.CustomUser.objects.change_password(id, password1)

        return super(CustomUserPasswordChangeForm, self).save(commit=False)

    class Meta:
        model = models.CustomUser
        fields = ('id', 'password',)


"""WATERCOURSES FORMS"""
class WaterCourseCreateForm(forms.ModelForm):

    class Meta:
        model = models.WaterCourse
        fields = '__all__'
