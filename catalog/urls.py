from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='home'),  # главная
    path('catalog/', views.catalog, name='catalog'),
    path('add-product/', views.add_product, name='add_product'),
    path('about/', views.about, name='about'),
    path('kompanijam/', views.kompanijam, name='kompanijam'),
    path('avtorskie-bukety/', views.avtorskie_bukety, name='avtorskie-bukety'),
    path('mono-duo-trio-bukety/', views.mono_duo_trio_bukety, name='mono-duo-trio-bukety'),
    path('korzini-cvetov/', views.korzini_cvetov, name='korzini-cvetov'),
    path('tsvety-v-korobkah/', views.tsvety_v_korobkah, name='tsvety-v-korobkah'),
    path('vazy/', views.vazy, name='vazy'),
    path('dostavka-i-oplata/', views.dostavka_i_oplata, name='dostavka-i-oplata'),
    path('politika-konfidentsialnosti/', views.politika_konfidentsialnosti, name='politika-konfidentsialnosti'),

    path('product/<int:id>/', views.product_detail, name='product-detail'),

    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    # path('dishes/', views.dish_list, name='dish_list'),
]
