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
    
    
@api_view(['POST'])
def calendar_view(request): # 캘린더 확인 (성공여부 계산)
    # date_day = request.data['datetime'].split('-')
    # find_userid = User.objects.get(username=request.data['id'])
    
    food_success_day = [0] * 30 # 성공 여부 월단위
    
    # 일별 먹은 칼로리
    today_cal = 0
    
    # user의 권장 칼로리
    user = User.objects.get(username=request.data['id'])
    PA_value_M = [1.0, 1.11, 1.25, 1.48]
    PA_value_W = [1.0, 1.12, 1.27, 1.45]
    
    if(user.users.sex == 1): # 여자 권장 칼로리
        goal_cal = round(354 - 6.91 * user.users.age + PA_value_W[user.users.pa] * (9.36 * user.users.weight + 726 * user.users.height * 0.01))
    else: # 남자 권장 칼로리 (호호혹시나 성별 표시 안하면 남자로 계산됨)
        goal_cal = round(662 - 9.53 * user.users.age + PA_value_M[user.users.pa] * (15.91 * user.users.weight + 539.6 * user.users.height * 0.01))
    
    
    # 날짜와 Id로 user_food 테이블에서 조회함
    # cal = user_food.objects.filter(user_id=find_userid.id, date__year=date_day[0], date__month=date_day[1]) # 날짜에 있는 데이터 개수에 따라 [0][1][2] 값으로 불러올 수 있음 (day는 date__day=date_day[2])
    
    # for i_date in range(1, 31):
    #     counts = user_food.objects.filter(user_id=find_userid.id, date__year=date_day[0], date__month=date_day[1], date__day=i_date).count() # 하룻동안 식단 개수
    #     for i_day in range(counts):
    #         cal = user_food.objects.filter(user_id=find_userid.id, date__year=date_day[0], date__month=date_day[1], date__day=i_date) # 날짜에 있는 데이터 개수에 따라 [0][1][2] 값으로 불러올 수 있음(있을때만)

    #         today_cal += cal[i_day].food_cal # 오늘 먹은 음식 칼로리 더하기
            
    #         if(counts == 3 and today_cal < goal_cal):
    #             food_success_day[i_date - 1] = 1

    #     today_cal = 0
    food_success_day = success_day_count(request.data['id'], request.data['datetime'], goal_cal)
        
    content = [
        {"date":1, "success":food_success_day[0]},
        {"date":2, "success":food_success_day[1]},
        {"date":3, "success":food_success_day[2]},
        {"date":4, "success":food_success_day[3]},
        {"date":5, "success":food_success_day[4]},
        {"date":6, "success":food_success_day[5]},
        {"date":7, "success":food_success_day[6]},
        {"date":8, "success":food_success_day[7]},
        {"date":9, "success":food_success_day[8]},
        {"date":10, "success":food_success_day[9]},
        {"date":11, "success":food_success_day[10]},
        {"date":12, "success":food_success_day[11]},
        {"date":13, "success":food_success_day[12]},
        {"date":14, "success":food_success_day[13]},
        {"date":15, "success":food_success_day[14]},
        {"date":16, "success":food_success_day[15]},
        {"date":17, "success":food_success_day[16]},
        {"date":18, "success":food_success_day[17]},
        {"date":19, "success":food_success_day[18]},
        {"date":20, "success":food_success_day[19]},
        {"date":21, "success":food_success_day[20]},
        {"date":22, "success":food_success_day[21]},
        {"date":23, "success":food_success_day[22]},
        {"date":24, "success":food_success_day[23]},
        {"date":25, "success":food_success_day[24]},
        {"date":26, "success":food_success_day[25]},
        {"date":27, "success":food_success_day[26]},
        {"date":28, "success":food_success_day[27]},
        {"date":29, "success":food_success_day[28]},
        {"date":30, "success":food_success_day[29]}
    ]
    return Response(content)


def success_day_count(id, datetime, goal_cal): # 성공 일수 세기 (성공 일 list 보냄)
    date_day = datetime.split('-')
    find_userid = User.objects.get(username=id)
    
    # 성공 여부 월단위
    food_success_day = [0] * 30
    # 일별 먹은 칼로리
    today_cal = 0
    
    # 날짜와 Id로 user_food 테이블에서 조회함
    # cal = user_food.objects.filter(user_id=find_userid.id, date__year=date_day[0], date__month=date_day[1]) # 날짜에 있는 데이터 개수에 따라 [0][1][2] 값으로 불러올 수 있음 (day는 date__day=date_day[2])
    
    for i_date in range(1, 31):
        counts = user_food.objects.filter(user_id=find_userid.id, date__year=date_day[0], date__month=date_day[1], date__day=i_date).count() # 하룻동안 식단 개수
        for i_day in range(counts):
            cal = user_food.objects.filter(user_id=find_userid.id, date__year=date_day[0], date__month=date_day[1], date__day=i_date) # 날짜에 있는 데이터 개수에 따라 [0][1][2] 값으로 불러올 수 있음(있을때만)

            today_cal += cal[i_day].food_cal # 오늘 먹은 음식 칼로리 더하기
            
            if(counts == 3 and today_cal < goal_cal):
                food_success_day[i_date - 1] = 1

        today_cal = 0
        
    return food_success_day
        
        
# 해당 날짜의 탄단지 비율, 아점저 칼로리, 목표 칼로리, 총 칼로리
@api_view(['POST'])
def calendar_day_info(request):
    date_day = request.data['datetime'].split('-') # 연도-월-일 까지 받음
    find_userid = User.objects.get(username=request.data['id']) # id 받음
    
    # 변수 넣어놓음
    # 아점저 칼로리
    today_cal = [0] * 3
    # 탄단지 총합
    total_carbo = 0
    total_protein = 0
    total_fat = 0
    # 총 칼로리
    total_cal = 0
    # 목표 칼로리
    PA_value_M = [1.0, 1.11, 1.25, 1.48]
    PA_value_W = [1.0, 1.12, 1.27, 1.45]
    
    if(find_userid.users.sex == 1): # 여자 권장 칼로리
        goal_cal = round(354 - 6.91 * find_userid.users.age + PA_value_W[find_userid.users.pa] * (9.36 * find_userid.users.weight + 726 * find_userid.users.height * 0.01))
    else: # 남자 권장 칼로리 (호호혹시나 성별 표시 안하면 남자로 계산됨)
        goal_cal = round(662 - 9.53 * find_userid.users.age + PA_value_M[find_userid.users.pa] * (15.91 * find_userid.users.weight + 539.6 * find_userid.users.height * 0.01))
    
    
    # 어케 해야하냐면 보내야하는게 탄단지 비율 아점저 -> 이게 아이디랑 날짜 매칭해서 User_food 테이블에서 가져오는거고..
    # 탄단지 비율은 [0][1][2] 더하는거고? [0]일 때 칼로리,[1]일 때 칼로리, [2]일 때 칼로리 가져오는거니끼
    
    # 하루 식단 id와 datetime으로 가져오기
    cal = user_food.objects.filter(user_id=find_userid.id, date__year=date_day[0], date__month=date_day[1], date__day=date_day[2])
    
    for i_day in range(cal.count()):
        today_cal[i_day] = cal[i_day].food_cal # 아점저 칼로리 리스트에 넣기
        
        total_carbo += cal[i_day].food_carbo
        total_protein += cal[i_day].food_protein
        total_fat += cal[i_day].food_fat
        
        total_cal += cal[i_day].food_cal
    
    totalNutrients = 0
    totalNutrients = total_carbo + total_protein + total_fat
    if totalNutrients == 0:
        totalNutrients = 1 # 1로 해놔야 에러 안뜸
        
    # 소숫점 둘째까지 탄단지 비율
    ratio_carbo = '%.2f%%'%(total_carbo/totalNutrients * 100.0)
    ratio_protein = '%.2f%%'%(total_protein/totalNutrients * 100.0)
    ratio_fat = '%.2f%%'%(total_fat/totalNutrients * 100.0)

        
    content = {
        'ratio_carbo' : ratio_carbo,
        'ratio_protein' : ratio_protein,
        'ratio_fat' : ratio_fat,
        'breakfast_cal' : today_cal[0],
        'lunch_cal' : today_cal[1],
        'dinner_cal' : today_cal[2],
        'total_cal' : total_cal,
        'goal_cal' : goal_cal
    }
    
    return Response(content)