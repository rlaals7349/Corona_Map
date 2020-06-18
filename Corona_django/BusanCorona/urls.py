"""BusanCorona URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from . import views, settings
from django.http import HttpResponseRedirect
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r : HttpResponseRedirect ( 'BS/')),
    path('BS/', include("BS.urls"))
    # path('menu1/', views.menu1, name='menu1'),
    # path('menu2/', views.menu2, name='menu2'),
    # path('menu3/', views.menu3, name='menu3'),
    # path('menu4/', views.menu4, name='menu4'),
]