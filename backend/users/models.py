from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    username = models.TextField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[-a-zA-Z0-9_]+$", message="Недопустимое имя пользователя"
            )
        ],
    )
    email = models.EmailField("email adress", unique=True, max_length=254)
    first_name = models.TextField(max_length=150)
    last_name = models.TextField(max_length=150)
