"""logserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', get_all_logs, name="get_all_logs"),
    path('daily', get_daily_logs, name="get_daily_logs"),
    path('warning', get_warning_logs, name="get_warning_logs"),
    path('error', get_error_logs, name="get_error_logs"),
    path('default', get_default_logs, name="get_default_logs"),
]
