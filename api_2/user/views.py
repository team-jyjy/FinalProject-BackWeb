from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from user import serializers
from . import models


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

        #token = Token.objects.create(user=user)
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

# 신체 활동 지수
# 성인여자 = 354 - 6.91 x 연령(세) + PA[9.36x체중(kg)+726x신장(m)]
# PA(신체활동계수): 1.0(비활동적), 1.12(저활동적), 1.27(활동적), 1.45(매우 활동적)

# 성인남자 = 662-9.53x연령(세) + PA[15.91 x 체중(kg) + 539.6 x 신장(m)]
# PA(신체활동계수) : 1.0(비활동적), 1.11(저활동적), 1.25(활동적), 1.48(매우 활동적)

@api_view(['GET']) # auth header를 넣어줘야함.
def Info(request):
    user = User.objects.get(pk=request.user.pk)
    PA_value_M = [1.0, 1.11, 1.25, 1.48]
    PA_value_W = [1.0, 1.12, 1.27, 1.45]
    
    if(user.users.sex == 1): # 여자 권장 칼로리
        goal_cal = round(354 - 6.91 * user.users.age + PA_value_W[user.users.pa] * (9.36 * user.users.weight + 726 * user.users.height * 0.01))
    else: # 남자 권장 칼로리 (호호혹시나 성별 표시 안하면 남자로 계산됨)
        goal_cal = round(662 - 9.53 * user.users.age + PA_value_M[user.users.pa] * (15.91 * user.users.weight + 539.6 * user.users.height * 0.01))
    
    if user.users.sex == 1:
        sex = '여자'
    else:
        sex = '남자'
        
    content = {
        'nickname': user.users.nickname,
        'height': user.users.height,
        'weight': user.users.weight,
        'age': user.users.age,
        'sex': sex,
        'goal_cal': goal_cal
    }
    return Response(content)



