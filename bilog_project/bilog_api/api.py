from django.contrib.auth.models import User


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import RegistrationSerializer

@api_view(['POST'])
def registration_view(request, format=None):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()            
            data['response'] = 'u successfully register'
            data['username'] = account.username
            token = Token.objects.get(user=account.username).key
            data['token'] = token
        else:
            data = serializer.errors
            return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data)



@api_view(['POST'])
def login_view(request, format=None):
    if request.method == 'POST':
        
        data = {}
        try:
            user = User.objects.get(username=request.POST['username'])
        except User.DoesNotExist:
            user=None

        if user != None and user.check_password(request.data['password']):
            token, created = Token.objects.get_or_create(user=user.pk)
            data['token'] = token.key
            data['username'] = user.username
            data['password'] = user.password
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'response': 'Invalid Username or Password'}
            return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data)

