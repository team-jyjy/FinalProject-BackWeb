from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view()), # 클래스뷰라서 as_view()사용
    path('login/', views.LoginView.as_view()),
    path('token/', views.Token_conf, name='Token_conf'),
    path('Info/',views.Info),
]