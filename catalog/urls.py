from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='home'),  # главная
    path('catalog/', views.catalog, name='catalog'),
    path('add-product/', views.add_product, name='add_product'),
    path('about/', views.about, name='about'),
]
