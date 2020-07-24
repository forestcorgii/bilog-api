from rest_framework.authtoken import views
from . import api
from django.urls import path, re_path



urlpatterns = [
    path('register/',api.registration_view),
    path('login/',api.login_view)
    # path('',UserDetail.as_view())
]

urlpatterns += [
     path('api-token-auth/', views.obtain_auth_token)
]