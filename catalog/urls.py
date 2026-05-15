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

    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),

    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('favorites/', views.favorites, name='favorites'),
    path('cart/', views.cart, name='cart'),

    path('cart/increase/<int:product_id>/', views.cart_increase, name='cart_increase'),
    path('cart/decrease/<int:product_id>/', views.cart_decrease, name='cart_decrease'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    # path('dishes/', views.dish_list, name='dish_list'),
]
