from django.urls import path

from members import views

app_name = 'members'

urlpatterns = [
    path('register/', views.custom_register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('update-email/', views.custom_update_email, name='update_email'),
]
