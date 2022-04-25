from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from django.http import HttpResponse
import requests


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        user = authenticate(username=email, password=password)
        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': "Email or Password are invalid, please check and try again"},
                        status=status.HTTP_401_UNAUTHORIZED)


class RandomNumberAPIView(GenericAPIView):

    def get(self, request):
        random_number_url = "http://www.randomnumberapi.com/api/v1.0/random?count=1"
        response = requests.get(random_number_url)
        return Response(response.json(), status=status.HTTP_200_OK)
