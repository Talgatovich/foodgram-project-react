from django.contrib.auth import get_user_model
from django.db import models
from users.models import User

#User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author",
        verbose_name="автор",
    )
    title = models.CharField(max_length=250)
