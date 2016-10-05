from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from profiles.forms import UserForm, ProfileForm
from .models import *


# Create your views here.
@login_required
def get_user_profile(request,username):
    user = User.objects.get(username=username)
    context = {"user": user}
    return render(request, 'profiles/user_profile.html', context)


class MyRegistrationForm(object):
    pass

@transaction.atomic
def register_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # This will load the Profile created by the Signal
            profile_form = ProfileForm(request.POST, instance=user.profile)  # Reload the profile form with the profile instance
            profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            profile_form.save()  # Gracefully save the form
            messages.success(request, 'Your account was succesfully created')
            return redirect('register_success')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'profiles/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def register_success(request):
    return render(request, 'profiles/register_success.html', {})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('register_success')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })