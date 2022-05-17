from scipy.fft import irfft
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
    
    # ir
    # 1개월~5개월까지 1.5%, 6개월~11개월 1.75%, 12개월~23개월까지 2.15%, 24~35 2.25%, 36개월~ 2.45%
    # 2022-1월부터 서비스가 시작되었다고 가정
    date_day = request.data['datetime'].split('-')
    date_day = list(map(int, date_day))
    print('dddddd : ', type(date_day[0]))
    ir = 1.5 # 기본 금리
    success_total_count = 0
    for i_year in range(2022, date_day[0] + 1):
        for i_month in range(1, 13):
            if i_year == date_day[0] and i_month == date_day[1] + 1:
                break
            if sum(success_day_count(request.user, str(i_year)+'-'+str(i_month), goal_cal)) >= 20:
                success_total_count += 1
                
    if success_total_count >= 6 and success_total_count < 12:
        ir = 1.75
    elif success_total_count >= 12 and success_total_count < 24:
        ir = 2.15
    elif success_total_count >= 24 and success_total_count < 36:
        ir = 2.25
    elif success_total_count >= 36:
        ir = 2.45
        
    content = {
        'nickname': user.users.nickname,
        'height': user.users.height,
        'weight': user.users.weight,
        'age': user.users.age,
        'sex': sex,
        'goal_cal': goal_cal,
        'success_day': success_day,
        'ir': ir
    }
    return Response(content)
    