from django.db.models import F
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import User
from users.serializers import CustomUserSerializer

from .models import (
    Favorite,
    Ingridients,
    Recipe,
    RecipeIngredients,
    ShoppingCart,
    Tag,
)


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngridientsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridients
        fields = ("id", "name", "measurement_unit")


class ShowRecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredients
        fields = ("id", "name", "measurement_unit", "amount")


class RecipesListSerializer(serializers.ModelSerializer):

    tags = TagListSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_ingredients(self, obj):
        ingredients = RecipeIngredients.objects.filter(recipe=obj)
        return ShowRecipeIngredientsSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context["request"]
        if request.user.is_anonymous:
            return False
        user_id = request.user.id
        favorite = Favorite.objects.all().filter(user=user_id, recipes=obj)
        return favorite.exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context["request"]
        if request.user.is_anonymous:
            return False
        user_id = request.user.id
        recipe_in_cart = ShoppingCart.objects.all().filter(
            user=user_id, recipe=obj
        )
        return recipe_in_cart.exists()


class RecipesIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingridients.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredients
        fields = ("id", "amount")


class RecipesCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = RecipesIngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def add_recipe_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient["id"]
            amount = ingredient["amount"]
            if RecipeIngredients.objects.filter(
                recipe=recipe, ingredient=ingredient_id
            ).exists():
                amount += F("amount")
            RecipeIngredients.objects.update_or_create(
                recipe=recipe,
                ingredient=ingredient_id,
                defaults={"amount": amount},
            )

    def create(self, validated_data):
        author = self.context.get("request").user
        tag_from_data = validated_data.pop("tags")
        ingredients_from_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_recipe_ingredients(ingredients_from_data, recipe)
        recipe.tags.set(tag_from_data)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        tag_from_data = validated_data.pop("tags")
        if tag_from_data:
            instance.tags.set(tag_from_data)

        ingredients_from_data = self.validated_data.pop("ingredients")
        instance.ingredients.clear()
        self.add_recipe_ingredients(ingredients_from_data, instance)
        instance.save()
        return instance

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get("ingredients")
        if ingredients == []:
            raise ValidationError("Необходимо выбрать хотя бы один ингредиент")
        for ingredient in ingredients:
            if int(ingredient["amount"] <= 0):
                raise ValidationError(
                    "Убедитесь, что это значение больше либо равно 1."
                )
        return data

    def to_representation(self, recipe):
        data = RecipesListSerializer(
            recipe, context={"request": self.context.get("request")}
        ).data
        return data


class ShowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class FavoriteSerializer(serializers.ModelSerializer):
    recipes = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = ("user", "recipes")

    def validate_recipes(self, data):
        user = self.context.get("request").user
        recipe = self.initial_data.get("recipes")
        if Favorite.objects.all().filter(user=user, recipes=recipe).exists():
            raise ValidationError("Этот рецепт у вас уже в избранном")
        return data

    def to_representation(self, instance):
        data = ShowRecipeSerializer(instance.recipes).data
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ShoppingCart
        fields = ("user", "recipe")

    def validate_recipe(self, data):
        user = self.context.get("request").user
        recipe = self.initial_data.get("recipe")
        if (
            ShoppingCart.objects.all()
            .filter(user=user, recipe=recipe)
            .exists()
        ):
            raise ValidationError("Этот рецепт уже в вашей корзине")
        return data

    def to_representation(self, instance):
        data = ShowRecipeSerializer(instance.recipe).data
        return data
