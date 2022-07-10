from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ingridients(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipe",
        verbose_name="автор",
    )
    tags = models.ManyToManyField(Tag, through="RecipeTag")
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to="recipes/media/",
        blank=False,
        null=False,
        verbose_name="Картинка",
    )
    ingredients = models.ManyToManyField(Ingridients, through="RecipeIngredients")
    text = models.CharField(max_length=500)
    cooking_time = models.CharField(max_length=20)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe")
    ingredient = models.ForeignKey(
        Ingridients, on_delete=models.PROTECT, related_name="ingredient"
    )
    amount = models.PositiveIntegerField(verbose_name="Количество")


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name="recipe_tag", on_delete=models.CASCADE
    )
    tags = models.ForeignKey(
        Tag, related_name="recipe_tag", on_delete=models.DO_NOTHING
    )


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite")
    recipes = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite_recipe"
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "recipes"], name="recipe_in_favorite_unique"
            )
        ]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shopping_cart"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_in_shopping_cart",
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "recipe"], name="recipe_in_shopping_cart")
        ]
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"
