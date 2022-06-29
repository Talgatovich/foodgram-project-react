from django.contrib.auth import get_user_model
from django.db import models

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
    tag = models.ForeignKey(
        Tag,
        on_delete=models.DO_NOTHING,
        related_name="tag",
        verbose_name="тэг",
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        'Картинка',
        blank=True
    )
    ingredients = models.ForeignKey(
        Ingridients,
        on_delete=models.CASCADE,
        related_name="ingridient",
        verbose_name="ингридиент",
    )
    text = models.CharField(max_length=500)
    cooking_time = models.CharField(max_length=20)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.name
