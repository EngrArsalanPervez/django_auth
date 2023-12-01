from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from members.forms import (
    CustomLoginForm,
    CustomRegisterForm,
    CustomUpdateEmailForm,
    CustomUpdatePasswordForm,
    CustomProfileForm,
)
from members.models import UserProfile


def custom_register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Check if the username is unique
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken.')
                return render(request, 'members/register.html', {'form': form})

            # Check if the email is unique
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'This email is already registered.')
                return render(request, 'members/register.html', {'form': form})

            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('core:homepage')
        else:
            messages.error(request, 'Registration Failed!')
            return render(request, 'members/register.html', {'form': form})
    else:
        form = CustomRegisterForm()
        return render(request, 'members/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('core:homepage')
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'members/login.html', {'form': form})
        else:
            messages.error(request, 'Login Failed!')
            return render(request, 'members/login.html', {'form': form})
    else:
        form = CustomLoginForm()
        return render(request, 'members/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('core:homepage')


def custom_update_email(request):
    if request.method == 'POST':
        form = CustomUpdateEmailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            if User.objects.exclude(email=request.user.email).filter(email=email).exists():
                form.add_error('email', 'This email is already registered.')
                return render(request, 'members/update_email.html', {'form': form})

            request.user.email = email
            request.user.save()
            return redirect('core:homepage')
        else:
            messages.error(request, 'Update Email Failed!')
            return render(request, 'members/update_email.html', {'form': form})
    else:
        form = CustomUpdateEmailForm(initial={'email': request.user.email})
        return render(request, 'members/update_email.html', {'form': form})


def custom_update_password(request):
    if request.method == 'POST':
        form = CustomUpdatePasswordForm(request.POST)

        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            password = form.cleaned_data['password']

            authenticated_user = authenticate(username=request.user.username, password=old_password)

            if authenticated_user is not None:
                request.user.set_password(password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect('core:homepage')
            else:
                form.add_error('old_password', 'Old Password Incorrect')
                return render(request, 'members/update_password.html', {'form': form})
        else:
            messages.error(request, 'Update Password Failed!')
            return render(request, 'members/update_password.html', {'form': form})
    else:
        form = CustomUpdatePasswordForm()
        return render(request, 'members/update_password.html', {'form': form})


def custom_profile(request):
    if request.method == 'POST':
        form = CustomProfileForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            profile_picture = form.cleaned_data['profile_picture']

            print(name, age, profile_picture)

            if UserProfile.objects.filter(user=request.user).exists():
                UserProfile.objects.filter(user=request.user).delete()

            UserProfile.objects.create(
                user=request.user,
                name=name,
                age=age,
                profile_picture=profile_picture,
            ).save()

            return redirect('core:homepage')
        else:
            messages.error(request, 'Update Profile Failed!')
            return render(request, 'members/profile.html', {'form': form})
    else:
        form = CustomProfileForm()
        return render(request, 'members/profile.html', {'form': form})
