from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    following = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class RegisterUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name')


class FollowCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор для добавления и удаления подписки на автора"""
    following = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Follow
        fields = ('user', 'following', )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=("user", "following")
            )
        ]

    def validate_following(self, value):
        user = self.context.get("request").user
        if user == value:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя!"
            )
        return value
    