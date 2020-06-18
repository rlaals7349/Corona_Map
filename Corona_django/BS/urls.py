from django.urls import path
from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('phar', views.phar, name='phar'),
    path('phar2', views.phar2, name='phar2'),
    path('More', views.More, name='More'),
    path('pharmacy_data', views.pharmacy_data, name='pharmacy_data'),
]
