from rest_framework import serializers
# from .models import  Account
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username','email',  'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
        
    def save(self):
        user = User(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            # middlename=self.validated_data['middlename'],
            # date_of_birth=self.validated_data['date_of_birth'],
            # username=self.validated_data['username'],
            email=self.validated_data['email'],
            )
        
        user.set_password(self.validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    


