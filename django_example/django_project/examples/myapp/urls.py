from django.urls import path
from . import views


urlpatterns = [
    path("", views.home),
    path("index", views.index),
    path("indeks", views.indeks),    
    path("details", views.details),
    path("<int:category_id>", views.getProductsCategoryId),
    path("<str:category>", views.getProductsCategory, name="products_by_category"),
]
 