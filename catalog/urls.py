from django.contrib import admin
from django.urls import path

from catalog.views import my_view
from catalog.views import my_view

urlpatterns = [
    path('admin/', my_view),

]