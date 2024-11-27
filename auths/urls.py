from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', login), 
    path('register', register),  
    path('me', profile_view, name='get_update_profile'),  
    path('password', change_password),
    path('refresh_token', refresh_token)
]
