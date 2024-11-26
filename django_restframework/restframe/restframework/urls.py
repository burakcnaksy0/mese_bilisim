from django.urls import path
from . import views

urlpatterns = [

    path("login", views.login, name="login"),
    path("deviceinfo", views.device_info, name="device_info")
]
