from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from users.permissions import UserPermission
from users.models import Users
from users.serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
import logging
import traceback


class UserView(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]


class LoginView(APIView):


    def post(self, request):
        requested_data = request.data
        ser_data = LoginSerializer(data=requested_data)
        if ser_data.is_valid():
            email = requested_data.get("email") 
            password = requested_data.get("password")
            try:
                user = Users.objects.get(email=email)
                if user.check_password(password):
                    ser_user = UserSerializer(user)
                    token = RefreshToken.for_user(user)
                    access_token = str(token.access_token)
                    refresh_token = str(token)
                    login(request, user)
                    response = {}
                    response = ser_user.data
                    response['access_token'] = access_token
                    response['refresh_token'] = refresh_token
                    return Response(response, status.HTTP_200_OK)    
                else:
                    return Response({"error": "Invalid username or password"}, status.HTTP_400_BAD_REQUEST)
            except:
                logging.error(traceback.format_exc())
                return Response({"error": "user not found, signup first!"}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(ser_data.errors, status.HTTP_400_BAD_REQUEST)
