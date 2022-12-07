from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.vars import (MSG_FOR_RESERVED_NAME, MSG_FOR_USER_NOT_FOUND,
                            RESERVED_NAMES_LIST)
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        if value in RESERVED_NAMES_LIST:
            raise serializers.ValidationError(MSG_FOR_RESERVED_NAME)
        return value


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор для модели администратора."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value in RESERVED_NAMES_LIST:
            raise serializers.ValidationError(MSG_FOR_RESERVED_NAME)
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для запроса токена."""
    username = serializers.CharField(max_length=200, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    def validate_username(self, value):
        if value in RESERVED_NAMES_LIST:
            raise serializers.ValidationError(MSG_FOR_RESERVED_NAME)
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(MSG_FOR_USER_NOT_FOUND)
        return value
