from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from project.sua.views.apis.serializer import LoginSerializer,UserSerializer

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                username = User.objects.get(username=serializer.validated_data['username']).username
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            user = authenticate(request, username=username, password=serializer.validated_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    userSerializer = UserSerializer(user, context={'request': request})
                    return Response(userSerializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)