from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from members.forms import (
    CustomLoginForm,
    CustomRegisterForm,
    CustomUpdateEmailForm,
)


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

            if User.objects.exclude(email= request.user.email).filter(email=email).exists():
                form.add_error('email', 'This email is already registered.')
                return render(request, 'members/update_email.html', {'form': form})

            request.user.email = email
            request.user.save()
            return redirect('core:homepage')
    else:
        form = CustomUpdateEmailForm(initial={'email': request.user.email})
        return render(request, 'members/update_email.html', {'form': form})
