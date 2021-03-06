from rest_framework.authtoken import views
from . import api
from django.urls import path, re_path

urlpatterns = [
    path('register/',api.registration_view),
    path('login/',api.login_view),
    path('send_message/', api.send_message),
    path('messages/<str:friendname>', api.list_chat_view),
    path('messages/', api.list_chat_preview),
    path('search_user/',api.search_user_view),
]

# urlpatterns += [
#      path('api-token-auth/', views.obtain_auth_token)
# ]