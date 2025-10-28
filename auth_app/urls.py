from django.urls import path
from .views import RegisterAPI, LoginAPI, FaceLoginAPI, LogoutAPI, UserListAPI, UserDetailAPI,UserProfileAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
   
]
