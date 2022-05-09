from django.db import models
from django.contrib.auth.models import User


class Family(models.Model):
    join_date = models.DateTimeField()
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users') # CASCADE 쓰면 delete 할 때 이 오브젝트를 참조하는 오브젝트도 같이 삭제
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True)
    height = models.IntegerField(blank=False)
    weight = models.IntegerField(blank=False)
    age = models.IntegerField(blank=False)
    sex = models.IntegerField(blank=False)
    PA = models.IntegerField(blank=False)
    
    