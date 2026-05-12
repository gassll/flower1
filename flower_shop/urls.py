from itertools import product

from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('',include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
