from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from user import serializers
from . import models
from foods.views import success_day_count, Goal_cal


class SignupView(APIView):
    def post(self, request):
        # DB검사
        if User.objects.filter(username=request.data['id']).exists():
            return Response({"message": "fail"}, status = status.HTTP_403_FORBIDDEN)
        
        user = User.objects.create_user(username=request.data['id'], password=request.data['password'])
        profile = models.Profile(
            user=user, 
            nickname=request.data['nickname'], 
            height=request.data['height'],
            weight=request.data['weight'],
            age=request.data['age'],
            sex=request.data['sex'],
            pa=request.data['pa']
        )

        user.save()
        profile.save()

        return Response({"message": "success"})
    
class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['id'], password=request.data['password'])

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"message": "fail"}, status = status.HTTP_403_FORBIDDEN)
        
            
@api_view(['GET',])
def Token_conf(request, format=None):
    content = {
        'user': str(request.user),
        'result' : 'Authenticated',
    }
    return Response(content)

@api_view(['POST']) # auth header를 넣어줘야함.
def Info(request):
    user = User.objects.get(username=request.user) # 토큰으로 ID 검색
    goal_cal = Goal_cal(request.user)
    
    if user.users.sex == 1:
        sex = '여자'
    else:
        sex = '남자'
    
    food_success_day = success_day_count(request.user, request.data['datetime'], goal_cal)
    success_day = sum(food_success_day)
    
    content = {
        'nickname': user.users.nickname,
        'height': user.users.height,
        'weight': user.users.weight,
        'age': user.users.age,
        'sex': sex,
        'goal_cal': goal_cal,
        'success_day': success_day,
        'ir':1.5
    }
    return Response(content)
    