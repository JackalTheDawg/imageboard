from django.contrib import admin
from django.urls import path, include
from core import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(urls)),
]
