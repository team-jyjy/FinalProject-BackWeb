from django.db import models
from django.contrib.auth.models import User


class food_info(models.Model):
    food_name = models.CharField(max_length=255) # 음식명
    food_cal = models.IntegerField() # 칼로리(kcal)
    food_protein = models.FloatField() # 단백질(g)
    food_fat = models.FloatField() # 지방(g)
    food_carbo = models.FloatField() # 탄수화물(g)
    food_sugar = models.FloatField() # 총당류(g)
    food_chole = models.FloatField() # 콜레스테롤(mg)
    food_na = models.FloatField() # 나트륨(mg)
    food_saturated_fat = models.FloatField() # 포화지방(g)
    food_trans_fat = models.FloatField() # 트랜스지방(g)


class user_food(models.Model): # user, food_name과 1대 다 관계
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_info')
    food_info = models.ForeignKey(food_info, on_delete=models.CASCADE, related_name='user')
    date = models.DateTimeField(auto_now_add=True) # 저장한 날짜
    food_type = models.IntegerField() # 아점저
    food_cal = models.IntegerField() # 칼로리
    food_protein = models.FloatField() # 단백질
    food_fat = models.FloatField() # 지방
    food_carbo = models.FloatField() # 탄수화물
    