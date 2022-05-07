# 웹 요청으로부터 데이터를 받을 때 그 데이터를 받아다가 확인하고 다시 건내줌
# view에서 데이터를 받아 넣어서 검증함
from random import choices
from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationUserSerializer(serializers.ModelSerializer):
    """
    ModelSerializer로 만듦
    """
    
    # password2는 따로 없기 때문에 추가로 만들어 주어야 한다.
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    height = serializers.IntegerField()
    weight = serializers.IntegerField()
    age = serializers.IntegerField()
    sex = serializers.CharField()
    
    
    class Meta:
        """
        메타 클래스에 필드, 모델 등을 설정하고 
        password 필드의 스타일을 정해준다
        """
        model = User
        #fields = ['username', 'email', 'password','password2']
        fields = ['username','password','password2','height','weight','age','sex']
        extra_kwargs = {
            'password' : {'write_only':True}
        }
    
    def save(self):
        """
        저장시 한번 더 확인!
        """
        account = User(
            # email = self.validated_data['email'],
            username = self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        height = self.validated_data['height']
        weight = self.validated_data['weight']
        age = self.validated_data['age']
        sex = self.validated_data['sex']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})
        account.set_password(password)
        account.save()
        return account

