from django.urls import path
from . import views

app_name = 'foods'

urlpatterns = [
    path('get_food_info/', views.get_food_info),
    path('update_user_food/', views.update_user_food), 
]