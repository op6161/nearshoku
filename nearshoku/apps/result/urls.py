from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result),
    path('detail', views.detail),
]