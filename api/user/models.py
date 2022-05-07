from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# settings.AUTH_USER_MODEL이 정의한 유저 모델에서
# post_save : 무언가 저장이 되고 난 다음이면
# @receiver 를 받아서 아래의 함수를 실행시키라는 의미
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=False, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)