from django.urls import path

from main_app import views

app_name = "mainapp"

urlpatterns = [
    path('', views.index, name='index'),
]