# Generated by Django 3.2.13 on 2022-07-14 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_recipetag_recipe_tags_unique'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='recipe_in_favorite_unique',
        ),
        migrations.RenameField(
            model_name='favorite',
            old_name='recipes',
            new_name='recipe',
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='recipe_in_favorite_unique'),
        ),
    ]
