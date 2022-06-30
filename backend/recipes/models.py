from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Ingridients(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    measurement_unit = models.CharField(max_length=100)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipe",
        verbose_name="автор",
    )
    tag = models.ManyToManyField(Tag)
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/', 
        blank=False, 
        null=False,
        verbose_name='Картинка'
    )
    ingredients = models.ManyToManyField(Ingridients)
    text = models.CharField(max_length=500)
    cooking_time = models.CharField(max_length=20)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='recipe_in_favorite_unique'
            )
        ]
