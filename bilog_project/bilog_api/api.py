from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics

from .serializers import RegistrationSerializer,ChatSerializer,ChatListSerializer,UserSearchResultSerializer
from .models import Chat


@api_view(['POST'])
def registration_view(request, format=None):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()            
            data['response'] = 'u successfully register'
            data['username'] = user.username
            token, created = Token.objects.get_or_create(user=user.pk)
            data['token'] = token.key
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


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_chat_view(request,friendname):
    if request.method == "GET":    
        queryset = Chat.objects.filter(sender=request.user,receiver=User.objects.get(username=friendname).id) 
        serializer = ChatSerializer(queryset,many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK,safe=False)
                
    queryset = {'Invalid Request'}
    return Response(queryset, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_chat_preview(request):
    if request.method == "GET":    
        queryset = Chat.objects.filter(sender=request.user).distinct('receiver')
        serializer = ChatSerializer(queryset,many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK,safe=False)
        
    queryset = {'Invalid Request'}
    return Response(queryset, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_message(request):
    if request.method == 'GET':
        response={}
        user = User.objects.get(username=request.GET['sender'])
        if user == request.user:
            data = {
                'sender': user.id,
                'receiver': User.objects.get(username=request.GET['receiver']).id,
                'content': request.GET['content']
            }
            serializer = ChatSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'reponse': 'galing galing',
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            'reponse': 'Invalid User Assignment',
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_user_view(request):
    if request.method == 'GET':
        response = {}
        data = User.objects.all().exclude(pk=request.user.id).filter(username__contains=request.GET['searchinput'])
        serializer=UserSearchResultSerializer(data,many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


