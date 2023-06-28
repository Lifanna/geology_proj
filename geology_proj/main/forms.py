from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from main import models
from django.contrib.auth.password_validation import validate_password
import os
from uuid import uuid4
from django.core.files import File


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = '__all__'


"""OBJECTS FORMS"""
class ObjectCreateForm(forms.ModelForm):
    used_enginery = forms.CharField(label="Используемая техника", required=False, widget=forms.Textarea)

    # mbu = forms.ModelChoiceField(label="МБУ", queryset=models.CustomUser.objects.all(), required=False)

    # pmbou = forms.ModelChoiceField(label="ПМБУ", queryset=models.CustomUser.objects.all(), required=False)

    class Meta:
        model = models.License
        fields = '__all__'
        exclude = ('watercourses', 'lines',)


class LicenseWaterCourseCreateForm(forms.ModelForm):
    class Meta:
        model = models.LicenseWaterCourse
        fields = ('is_primary', 'license', 'watercourse', 'parent_watercourse',)


class LicenseWaterCourseRemoveForm(forms.ModelForm):
    watercourse = forms.MultipleChoiceField()

    class Meta:
        model = models.LicenseWaterCourse
        fields = '__all__'



class LineLicenseWaterCourseCreateForm(forms.ModelForm):
    class Meta:
        model = models.LineLicenseWaterCourse
        fields = ('watercourse', 'line', 'license',)


class ObjectUpdateForm(forms.ModelForm):
    used_enginery = forms.CharField(label="Используемая техника", required=False, widget=forms.Textarea)

    # mbu = forms.ModelChoiceField(label="МБУ", queryset=models.CustomUser.objects.all(), required=False)

    # pmbou = forms.ModelChoiceField(label="ПМБУ", queryset=models.CustomUser.objects.all(), required=False)

    class Meta:
        model = models.License
        # fields = (
        #     'short_name',
        #     'name',
        #     'geologist',
        #     'status',
        #     'used_enginery',
        #     'mbu',
        #     'pmbou',
        #     # 'watercourses',
        #     'comment',
        # )
        fields = '__all__'
        exclude = ('watercourses', 'lines',)
    
    # watercourses = forms.ModelMultipleChoiceField(
    #     queryset=models.WaterCourse.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )


"""TASKS FORMS"""
class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        exclude = ('wells', 'images',)


class TaskUpdateForm(forms.ModelForm):
    images = forms.ImageField(label="Фотографии", widget=forms.FileInput(attrs={'multiple': True}), required=False)

    def save(self):
        for name in self.files.getlist('images'):
            task_image_single = models.TaskImageSingle()
            _, ext = os.path.splitext(name.name)
            newname = f'{uuid4()}{ext}'

            task_image_single.image.save(
                os.path.basename(newname),
                File(name)
            )
            
            task_image = models.TaskImage(
                task = self.instance,
                task_image_single = task_image_single,
            )
            task_image.save()

        return super().save(commit=False)

    class Meta:
        model = models.Task
        fields = (
            'short_name',
            'description',
            'license',
            'watercourse',
            'line',
            # 'wells',
            'images',
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
            # 'team',
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


"""LINES FORMS"""
class LineCreateForm(forms.ModelForm):

    class Meta:
        model = models.Line
        fields = '__all__'


"""WELLS FORMS"""
class WellCreateForm(forms.ModelForm):
    class Meta:
        model = models.Well
        fields = '__all__'
        exclude = ('pillar_photo',)


class WellUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Well
        fields = (
            'name',
            'description',
            'comment',
            'line',
            'x',
            'y',
            'z',
        )


class WellTaskCreateForm(forms.ModelForm):
    class Meta:
        model = models.WellTask
        fields = '__all__'
        # exclude = ('watercourses', 'lines',)


"""LAYERS FORMS"""
class LayerCreateForm(forms.ModelForm):
    class Meta:
        model = models.Layer
        fields = '__all__'


class LayerUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Layer
        fields = (
            'name',
        )


class DocumentsCreateForm(forms.ModelForm):
    class Meta:
        model = models.Documentation
        fields = (
            'license',
            'watercourse',
            'line',
            'well',
        )


class MineCreateForm(forms.ModelForm):
    class Meta:
        model = models.Mine
        fields = (
            'license',
            'watercourse',
            'line',
            'wells',
            'address',
        )
