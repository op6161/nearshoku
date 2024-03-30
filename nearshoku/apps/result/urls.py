from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
    path('detail', views.detail),
]