from django.contrib.auth import get_user_model, login, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        # Added explicit registration status response for the frontend:
        # if the username already exists, return a clear message and flags
        # without creating another user.
        username = request.data.get('username')
        if username and User.objects.filter(username=username).exists():
            return Response(
                {
                    'message': 'User with this username already exists.',
                    'user_exists': True,
                    'user_created': False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        # Added structured validation failure response so the frontend can show
        # a generic registration message and still inspect field-level errors.
        if not serializer.is_valid():
            return Response(
                {
                    'message': 'User could not be created.',
                    'user_exists': False,
                    'user_created': False,
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        # Added success metadata while keeping user fields at the top level of
        # the response, so existing clients can still read id/username/email.
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
        # Added login failure message and boolean status for invalid credentials
        # or missing fields, instead of returning only serializer errors.
        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Invalid username or password.',
                    'login_success': False,
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.validated_data['user']
        login(request, user)
        # Added login success message and flag for the frontend after Django
        # creates the authenticated session.
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
