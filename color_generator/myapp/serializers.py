from rest_framework import serializers
from .models import Colours

class ColoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colours
        fields = ['id','user_name', 'colours']

    def validate_user_name(self, value):
        if not value:
            raise serializers.ValidationError("User name is required.")
        return value

    def validate_colours(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Colours must be a list.")
        if len(value) != 5:
            raise serializers.ValidationError("Colours array must contain exactly 5 items.")
        return value



from rest_framework import serializers

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username' ,'email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username' ,'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)