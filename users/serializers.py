import re
import time

import pyotp
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password2 = serializers.CharField(
        help_text=(
            "The password can not start with a digit, underscore or special character and must contain at least one digit. Password length between 8 to 20"
        )
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] == data["password2"] and re.match(
            r"^(?=[^\d_].*?\d)\w(\w|[!@#$%]){7,20}", data["password"]
        ):
            return data
        elif not re.match(r"^(?=[^\d_].*?\d)\w(\w|[!@#$%]){7,20}", data["password"]):
            raise serializers.ValidationError("Password isn't strong enough.")
        else:
            raise serializers.ValidationError("Password doesn't match.")

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        otp = pyotp.TOTP("base32secret3232").now()
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=email,
            password=password,
            otp=otp,
        )
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "email",
            "password",
            "is_active",
            "is_staff",
            "otp",
        )
