from django.contrib.auth import login, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # Structured validation failure response so the frontend can show a generic
        # registration message and still inspect field-level errors.
        if not serializer.is_valid():
            username_errors = serializer.errors.get('username', [])
            user_exists = any(
                getattr(error, 'code', None) == 'unique'
                for error in username_errors
            )
            return Response(
                {
                    'message': 'User could not be created.',
                    'user_exists': user_exists,
                    'user_created': False,
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        # Send metadata while keeping user fields at the top level of the response.
        data = dict(UserSerializer(user).data)
        data['message'] = 'User created successfully.'
        data['user_exists'] = False
        data['user_created'] = True
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            has_credentials = (
                'username' not in serializer.errors
                and 'password' not in serializer.errors
            )
            message = (
                'Invalid username or password.'
                if has_credentials
                else 'Username and password are required.'
            )
            return Response(
                {
                    'message': message,
                    'login_success': False,
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.validated_data['user']
        login(request, user)
        # Send success message and flag after creating the session.
        data = dict(UserSerializer(user).data)
        data['message'] = 'Login successful.'
        data['login_success'] = True
        return Response(data)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
