# Generated by Django 3.2.13 on 2022-07-13 18:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email адрес'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.TextField(max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.TextField(max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.TextField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Недопустимое имя', regex='^[-a-zA-Z0-9_]+$')], verbose_name='логин'),
        ),
    ]
