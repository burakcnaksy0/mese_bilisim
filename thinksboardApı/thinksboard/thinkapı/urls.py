from django.urls import path
from . import views

urlpatterns = [
    path("login", views.userlogın, name="loginpage"),
    path("device", views.devicePrefer, name="device_ınfo"),
    path('export_data', views.export_data, name='export_data'),
    path('send-telemetry/<str:device_id>/', views.send_random_telemetry, name='send_telemetry'),
    path('api/telemetry/', views.get_random_telemetry, name='get_random_telemetry'),

]
