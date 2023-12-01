from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse


@login_required
def homepage(request):
    return render(request, 'core/homepage.html')


@login_required
def contact(request):
    return render(request, 'core/contact.html')
