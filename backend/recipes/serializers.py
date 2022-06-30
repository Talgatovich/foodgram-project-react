from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import Ingridients, Recipe, Tag


class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngridientsListSerializer(serializers.ModelSerializer):
    amount = serializers.CharField(source='quantity')
    class Meta:
        model = Ingridients
        fields = ("id", "name", "measurement_unit", 'amount')


class RecipesListSerializer(serializers.ModelSerializer):
    tag = TagListSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngridientsListSerializer(many=True)
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
        ) #  добавить потом "is_favorited", "is_in_shopping_cart"