from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import RegistrationSerializer, LoginSerializer


# In RegistrationAPIView, serializer.is_valid() is implicitly called by the CreateAPIView when handling the POST
# request. The perform_create method is for adding additional operations after the object has been validated and
# created. In LoginAPIView, since it’s a custom operation and not a standard model operation like
# create/update/delete, serializer.is_valid() is called explicitly to ensure the data is valid before proceeding with
# the login process.
class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_201_CREATED, headers=headers)


# The line headers = self.get_success_headers(serializer.data) in a Django Rest Framework (DRF) view is
# used to generate a set of HTTP headers that should be included in the response after a successful operation,
# typically a POST request that creates a new resource.
# The line headers = self.get_success_headers(serializer.data) in your DRF view is about enhancing the
# HTTP response with useful headers
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
