from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    
    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', "is_subscribed")
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        following = obj.follower.filter(user=obj, following=user)
        
        return following.exists()
    

class RegisterUserSerializer(UserCreateSerializer):
    """ Сериализатор для регистрации пользователя"""
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name')


class FollowCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор для добавления и удаления подписки на автора"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Follow
        fields = ('user', 'following')
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


class FollowingRecipesSerializers(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(serializers.ModelSerializer):
    '''
    Возвращает пользователей, на которых подписан текущий пользователь.
    В выдачу добавляются рецепты.
    '''
    is_subscribed = serializers.SerializerMethodField()
    recipe = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipe',
            'is_subscribed',
            'recipes_count'
        )
        read_only_fields = fields

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        following = obj.follower.filter(user=obj, following=user)
        return following.exists()
    
    def get_recipe(self, obj):
        request = self.context.get('request')
        context = {'request': request}
        recipe = obj.recipe.all()
        return FollowingRecipesSerializers(recipe, context=context, many=True).data
    
    def get_recipes_count(self, obj):
        count = obj.recipe.all().count()
        return count
