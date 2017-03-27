from ajax_select import make_ajax_field
from ajax_select.fields import AutoCompleteField
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput
from profiles.models import Profile, Application


class UserForm(UserCreationForm):
    error_messages = {'password_incorrect':
                          "Passordet stemmer ikke, prøv igjen", 'required': 'Mangler ditt gamle passord',
                      'password_mismatch': 'Passordene var ulike, prøv igjen'}

    username = forms.CharField(label="Brukernavn")
    email = forms.EmailField(required=True, label="Epost")
    first_name = forms.CharField(required=True, label="Fornavn")
    last_name = forms.CharField(required=True, label="Etternavn")
    password1 = CharField(widget=PasswordInput(),required=True, label="Passord")
    password2 = CharField(widget=PasswordInput(),required=True, label="Bekreft passord")

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

class MyAuthenticationForm(AuthenticationForm):
    username = CharField(label="Brukernavn")
    password = CharField(widget=PasswordInput())

    error_messages = {
        'invalid_login':
            "Kontoen eksisterer ikke, eller kombinasjonen av brukernavn og passord er feil."}


class PasswordChangeCustomForm(PasswordChangeForm):
    error_messages = {'password_incorrect':
                          "Passordet stemmer ikke", 'required': 'Mangler ditt gamle passord',
                      'password_mismatch': 'Passordene var ulike'}

    old_password = CharField(label='Gammelt passord',
                             widget=PasswordInput(attrs={
                                 'class': 'form-control'}))

    new_password1 = CharField(label='Nytt passord',
                              widget=PasswordInput(attrs={
                                  'class': 'form-control'}))

    new_password2 = CharField(label='Bekreft nytt passord', widget=PasswordInput(attrs={'class': 'form-control'}))


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

class ProfileRegisterForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('institute',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = ('institute', 'coursesToTake',)

    coursesToTake = make_ajax_field(Profile, 'coursesToTake', 'homeCourse', help_text=None,
                                    required=False)


class CoursesToTakeForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = ('coursesToTake',)

    coursesToTake = AutoCompleteField('singleHomeCourse', help_text=None, required=True, attrs={"placeholder":"Søk på fagnavn/kode"})


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = ('institute', 'coursesToTake', 'saved_course_matches', 'saved_courses',)

    coursesToTake = make_ajax_field(Profile, 'coursesToTake', 'homeCourse', help_text="Please enter your course taken",
                                    required=False)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = {'course_matches', 'comment'}


def make_application_form(user,application):
    class ApplicationForm(forms.ModelForm):
        class Meta:
            model = Application
            fields = {'course_matches','comment'}


        course_matches = forms.ModelMultipleChoiceField(queryset=user.profile.saved_course_matches, label="Endre med fagkoblinger fra din profil")
        comment = forms.CharField(initial=application.comment, label="Kommentar")
    return ApplicationForm