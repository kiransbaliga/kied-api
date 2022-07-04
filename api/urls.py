from django.urls import path
from .views import *

urlpatterns=[
    path('login/', login_view, name='login'),
    path('register/', create_user_view, name='register'),
]