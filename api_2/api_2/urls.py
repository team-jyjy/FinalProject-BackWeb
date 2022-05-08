from django.urls import path, include
from django.contrib import admin
from user.views import Token_conf, What

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("user.urls")),
    path('api/test/', Token_conf, name='Token_conf'),
    # path('what/',What)
]
