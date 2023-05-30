from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="username already taken.",
                lookup="iexact",
            )
        ]
    )
    email = serializers.CharField(
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="email already registered.",
                lookup="iexact",
            )
        ],
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(required=False)
    is_employee = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        if validated_data["is_employee"] is True:
            return User.objects.create_superuser(**validated_data)
        return User.objects.create_user(**validated_data)
    
    def update(self, instance: User, validated_data: dict):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
