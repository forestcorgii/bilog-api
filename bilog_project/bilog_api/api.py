from django.contrib.auth.models import User


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import RegistrationSerializer,LoginSerializer

@api_view(['POST'])
def registration_view(request, format=None):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()            
            data['response'] = 'u successfully register'
            data['username'] = account.username
        else:
            data = serializer.errors
            return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def login_view(request, format=None):
    if request.method == 'POST':
        # serializer = LoginSerializer(data=request.data)

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



# class CustomAuthToken(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         account = User.objects.get(username=request.POST['username'])
#         token, created = Token.objects.get_or_create(user=account.username)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })


# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def example_view(request, format=None):
#     content = {
#         'user': unicode(request.user),  # `django.contrib.auth.User` instance.
#         'auth': unicode(request.auth),  # None
#     }
#     return Response(content)

# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_fields = ['id']


