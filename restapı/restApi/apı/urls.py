from django.urls import path
from . import views

urlpatterns = [
    path('', views.books, name="bookss"),
    path('<int:id>', views.book, name="thebook")

]
