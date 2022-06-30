from django.contrib import admin

from .models import Favorite, Ingridients, Recipe, Tag

admin.site.register(Recipe)
admin.site.register(Ingridients)
admin.site.register(Tag)
admin.site.register(Favorite)
