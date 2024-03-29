# Generated by Django 3.2.13 on 2022-07-14 09:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_rename_ingridients_ingridient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredients',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='recipe_ingredient_unique'),
        ),
    ]
