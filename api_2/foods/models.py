from django.db import models


class food_info(models.Model):
    food_name = models.CharField(max_length=255) # 음식명
    food_cal = models.IntegerField() # 칼로리(kcal)
    food_protein = models.FloatField() # 단백질(g)
    food_fat = models.FloatField() # 지방(g)
    food_carbo = models.FloatField() # 탄수화물(g)
    food_sugar = models.FloatField() # 총당류(g)
    food_chole = models.FloatField() # 콜레스테롤
    food_na = models.FloatField() # 나트륨(mg)
    food_saturated_fat = models.FloatField() # 포화지방(g)
    food_trans_fat = models.FloatField() # 트랜스지방(g)
