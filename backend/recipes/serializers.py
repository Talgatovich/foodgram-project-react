from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import Favorite, Ingridients, Recipe, RecipeIngredients, Tag


class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngridientsListSerializer(serializers.ModelSerializer):

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


class RecipesCreateSerializer(serializers.ModelSerializer):
    
    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
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
    
    def create(self, validated_data):
        author = self.context.get('request').user
        tag_from_data = validated_data.pop('tag')
        ingredients_from_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        for ingredient in ingredients_from_data:
            current_ingredient, status = Ingridients.objects.get_or_create(
                **ingredient
            )
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=current_ingredient
            )
        recipe.tag.set(tag_from_data)
        return recipe
        
