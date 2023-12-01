from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from members.models import UserProfile


@login_required
def homepage(request):
    name = ''
    age = ''
    profile_picture = ''

    if UserProfile.objects.filter(user=request.user).exists():
        profile = UserProfile.objects.get(user=request.user)
        name = profile.name
        age = profile.age
        profile_picture = profile.profile_picture

    return render(request, 'core/homepage.html', {
        'name': name,
        'age': age,
        'profile_picture': profile_picture
    })


@login_required
def contact(request):
    return render(request, 'core/contact.html')
