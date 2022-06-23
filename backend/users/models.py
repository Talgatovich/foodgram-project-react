from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.TextField(max_length=150, unique=True)    
    email = models.EmailField("email adress", unique=True, max_length=254)
    first_name = models.TextField(max_length=150)
    last_name = models.TextField(max_length=150)
