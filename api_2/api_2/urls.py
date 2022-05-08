from django.urls import path, include
from django.contrib import admin
from user.views import Token_conf, Info

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("user.urls")),
    path('api/test/', Token_conf, name='Token_conf'),
    path('Info/',Info)
]
