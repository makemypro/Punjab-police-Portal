from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from drowsiness_detection_ml.drowsiness_detetction.drowsiness_detection import Read_Frame


# Class based view to Get User Details using Token Authentication
# class UserDetailAPI(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (AllowAny,)
#
#     def get(self, request, *args, **kwargs):
#         user = request.user.id
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#
# # Class based view to register user
# class RegisterUserAPIView(generics.CreateAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer
#

class DriverAPIView(APIView):

    def get(self, request):
        print("Request----------------->")
        if request.query_params.get('is_detect'):
            Read_Frame()
        return Response({"OK": 2})

