from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='home'),  # главная

    path('catalog/', views.catalog, name='catalog'),
    path('catalog/category/<slug:slug>/', views.category_detail, name='category_detail'),

    path('product/<int:id>/', views.product_detail, name='product-detail'),

    path('add-product/', views.add_product, name='add_product'),
    path('about/', views.about, name='about'),
    path('kompanijam/', views.kompanijam, name='kompanijam'),
    path('dostavka-i-oplata/', views.dostavka_i_oplata, name='dostavka-i-oplata'),
    path('politika-konfidentsialnosti/', views.politika_konfidentsialnosti, name='politika-konfidentsialnosti'),

    # path('dishes/', views.dish_list, name='dish_list'),
]
