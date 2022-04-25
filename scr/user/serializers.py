from .models import User, validate_password
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, validators=[validate_password], write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, validators=[validate_password], write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        read_only_fields = ['token']
