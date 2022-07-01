from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import Favorite, Ingridients, Recipe, Tag


class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngridientsListSerializer(serializers.ModelSerializer):
    amount = serializers.CharField(source='quantity')

    class Meta:
        model = Ingridients
        fields = ("id", "name", "measurement_unit", 'amount')


class RecipesFavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )


class FavoriteSerializer(serializers.ModelSerializer):

    recipe = RecipesFavoriteListSerializer
    
    class Meta:
        model = Favorite
        fields = ("id", "user", "recipe",) #  '__all__' #('recipe',)


class RecipesListSerializer(serializers.ModelSerializer):
    
    tag = TagListSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngridientsListSerializer(many=True)
    image = Base64ImageField()
    
    class Meta:
        model = Recipe
        fields = (
            "id",
            "tag",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time"
        )  #  добавить потом "is_favorited", "is_in_shopping_cart"


class RecipesIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridients
        fields = ('id', 'amount')


class RecipesCreateEditSerializer(serializers.ModelSerializer):
    
    tag = serializers.PrimaryKeyRelatedField(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipesIngredientSerializer(many=True)
    image = Base64ImageField()
    
    class Meta:
        model = Recipe
        fields = (
            "id",
            "tag",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time"
        )  #  добавить потом "is_favorited", "is_in_shopping_cart"
