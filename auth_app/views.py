
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import User
import os
from rest_framework.permissions import AllowAny
from .utils import compare_face
import face_recognition
import uuid
import os
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser



class RegisterAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "Compte créé avec succès !",
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPI(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": f"Bienvenue {user.username} !",
                "user": UserSerializer(user).data,  # maintenant is_superuser est inclus
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response({
            "success": False,
            "message": "Nom d'utilisateur ou mot de passe invalide."
        }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPI(APIView):

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Nécessite rest_framework_simplejwt.token_blacklist
            return Response({"success": True, "message": "Déconnecté avec succès"})
        except Exception:
            return Response({"error": "Token invalide ou déjà blacklisted"}, status=400)
        
class UserListAPI(APIView):
    permission_classes = [IsAdminUser]  # seulement les superusers

    def get(self, request):
        users = User.objects.all().order_by("-id")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)