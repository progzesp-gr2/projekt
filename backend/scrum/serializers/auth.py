from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['username'],
            password=attrs['password'],
        )
        if user is None:
            raise serializers.ValidationError('Invalid username or password.')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = fields
