from rest_framework import serializers

from .models import Ingridients, Recipe, Tag


class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngridientsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingridients
        fields = ("id", "name", "measurement_unit")

class RecipesListSerializer(serializers.ModelSerializer):
    
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
        ) # добавить потом "is_favorited", "is_in_shopping_cart"
        


