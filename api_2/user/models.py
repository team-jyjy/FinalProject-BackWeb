from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model): # 한 유저당 1개의 프로필을 가지므로 oneTooneField 사용
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users') # CASCADE 쓰면 delete 할 때 이 오브젝트를 참조하는 오브젝트도 같이 삭제
    nickname = models.CharField(max_length=20) # 한글은 5글자까지 가능
    height = models.IntegerField(blank=False)
    weight = models.IntegerField(blank=False)
    age = models.IntegerField(blank=False)
    sex = models.IntegerField(blank=False)
    pa = models.IntegerField(blank=False)
    