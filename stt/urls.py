# this is urls file for django app

import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from stt import views


urlpatterns = [
    path('file/', views.upload_file, name='upload_file'),
]