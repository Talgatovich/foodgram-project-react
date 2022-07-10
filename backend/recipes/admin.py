from django.contrib import admin

from .models import (
    Favorite,
    Ingridients,
    Recipe,
    RecipeIngredients,
    RecipeTag,
    ShoppingCart,
    Tag,
)


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeTagInline, RecipeIngredientsInline)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingridients)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(RecipeIngredients)
admin.site.register(ShoppingCart)
