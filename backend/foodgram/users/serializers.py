from re import match

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import (SerializerMethodField,
                                        ValidationError,
                                        )

from .models import Follow

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'password'
                  )
        write_only_fields = ('password',)

    def validate_username(self, value):
        if not match(r'[\w.@+\-]+', value):
            raise ValidationError('Логин указан некорректно')
        return value


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed'
                  )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Follow.objects.filter(
            user=request.user,
            author=obj.id
        ).exists()
