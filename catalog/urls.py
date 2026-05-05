from django.contrib import admin
from django.urls import path

from views import my_view

urlpatterns = [
    path('catalog/admin', my_view),
]