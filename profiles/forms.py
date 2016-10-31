from ajax_select import make_ajax_field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from profiles.models import Profile


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()

        return user



class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        exclude = ['password']

    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()

        return user



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = ('institute','coursesToTake',)

    coursesToTake = make_ajax_field(Profile, 'coursesToTake', 'homeCourse', help_text="Please enter your course taken",required=False)

