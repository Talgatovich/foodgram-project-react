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
    list_display = ("name", "author", "favorite_recipe")
    list_filter = (
        "name",
        "author",
        "tags",
    )

    def favorite_recipe(self, obj):
        return obj.favorite_recipe.all().count()


class IngridientsAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "recipe", "amount")
    list_filter = (
        "ingredient",
        "recipe",
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    list_filter = ("user", "recipe")


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    list_filter = ("name", "slug")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingridients, IngridientsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
