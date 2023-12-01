from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('contact/', views.contact, name='contact'),
]
