from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index),
    path('result', views.result),
    path('detail', views.detail),
]