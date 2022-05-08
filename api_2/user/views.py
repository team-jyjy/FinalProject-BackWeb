from cProfile import Profile
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
        user = User.objects.create_user(username=request.data['id'], password=request.data['password'])
        profile = models.Profile(user=user, height=request.data['height'],
        weight=request.data['weight'],
        age=request.data['age'],
        sex=request.data['sex'])

        user.save()
        profile.save()

        token = Token.objects.create(user=user)
        return Response({"Token": token.key})
    
class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['id'], password=request.data['password'])
        if user is not None:
            token = Token.objects.get(user=user)
            return Response({"Token": token.key})
        else:
            return Response(status=401)
        
@api_view(['GET',])
def Token_conf(request, format=None):
    content = {
        'user': str(request.user),
        'result' : 'Authenticated',
    }
    return Response(content)

from django.contrib.auth import get_user_model
from django.core import serializers
@api_view(['GET',])
def Info(request):
    user = User.objects.get(pk=request.user.pk)
    content = {
        'height': user.users.height,
        'weight': user.users.weight,
        'age': user.users.age,
        'sex':user.users.sex
    }
    return Response(content)