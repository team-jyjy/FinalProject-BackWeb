from django.contrib import admin
from django.urls import path
from user.views import registration_view, example_view
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', registration_view, name='register_user'),
    path('api/user/login/', obtain_auth_token, name='login'),
    path('api/test/', example_view, name='example_view'),
]
