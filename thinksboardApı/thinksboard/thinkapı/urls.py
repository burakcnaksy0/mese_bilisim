from django.urls import path
from . import views

urlpatterns = [
    path("login", views.userlogın, name="loginpage"),
    path("device", views.devicePrefer, name="device_ınfo"),
    path('export_data', views.export_data, name='export_data'),
]
