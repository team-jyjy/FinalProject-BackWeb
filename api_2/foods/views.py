from django.shortcuts import render
from rest_framework.response import Response
from .models import food_info
from rest_framework.decorators import api_view


@api_view(['POST'])
def get_food_info(request): # 음식 올렸을 때 상세 정보 받아오기

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
