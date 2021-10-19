from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from styleguide_example.api.mixins import ApiAuthMixin
from styleguide_example.users.models import BaseUser
from styleguide_example.users.selectors import user_get_login_data
from styleguide_example.authentication.services import send_password_reset_email, user_reset_password


class UserLoginApi(APIView):
    """
    Following https://docs.djangoproject.com/en/3.1/topics/auth/default/#how-to-log-a-user-in
    """
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(request.user)
        user = authenticate(request, **serializer.validated_data)
        print(user)

        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)

        data = user_get_login_data(user=user)
        session_key = request.session.session_key

        return Response({
            'session': session_key,
            'data': data
        })


class UserLogoutApi(APIView):
    def get(self, request):
        logout(request)

        return Response()

    def post(self, request):
        logout(request)

        return Response()


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request):
        data = user_get_login_data(user=request.user)

        return Response(data)


class UserPasswordResetApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = get_object_or_404(BaseUser, email=email)

        send_password_reset_email(user=user)

        return Response(status=status.HTTP_200_OK)


class UserPasswordResetConfirmApi(APIView):
    class InputSerializer(serializers.Serializer):
        uid = serializers.IntegerField() # User id
        token = serializers.CharField()
        new_password = serializers.CharField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(BaseUser, pk=serializer.validated_data['uid'])

        user_reset_password(
            user=user,
            token=serializer.validated_data['token'],
            password=serializer.validated_data['new_password']
        )

        return Response(status=status.HTTP_200_OK)
