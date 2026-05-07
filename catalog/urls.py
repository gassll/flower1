from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_view, name='categories'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
]