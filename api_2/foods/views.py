from numpy import require
from rest_framework.response import Response
from .models import food_info, user_food
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST
from rest_framework import status
from django.contrib.auth.models import User


@api_view(['POST'])
def get_food_info(request): # 음식 올렸을 때 상세 정보 받아오기
    if not food_info.objects.filter(food_name=request.data['food_name']).exists():
        return Response({'message':'fail'}, status = status.HTTP_403_FORBIDDEN)
    
    info = food_info.objects.get(food_name=request.data['food_name'])
    content = {
        'food_cal': info.food_cal,
        'food_protein': info.food_protein,
        'food_fat': info.food_fat,
        'food_carbo': info.food_carbo,
        'food_sugar': info.food_sugar,
        'food_chole': info.food_chole,
        'food_na': info.food_na,
        'food_satarated_fat': info.food_saturated_fat,
        'food_trans_fat': info.food_trans_fat,
    }
    return Response(content)


@api_view(['POST'])
@require_POST
def update_user_food(request): # 먹은거 저장
    if not User.objects.filter(username=request.data['id']).exists(): # userID 존재하지 않음
        return Response({"message": "fail"}, status = status.HTTP_403_FORBIDDEN)
    
    
    info = food_info.objects.get(food_name=request.data['food_name'])

    user_foods = user_food(
        user=User.objects.get(username = request.data['id']), 
        food_info=food_info.objects.get(food_name = request.data['food_name']), 
        food_type=request.data['food_type'], 
        food_cal=info.food_cal,
        food_protein=info.food_protein, 
        food_fat =info.food_fat, 
        food_carbo=info.food_carbo,
    )
    
    user_foods.save()
    
    return Response({"message": "success"})
    
    
    

