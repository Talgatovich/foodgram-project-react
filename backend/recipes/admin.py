from django.contrib import admin

from .models import (
    Favorite,
    Ingridient,
    Recipe,
    RecipeIngredients,
    RecipeTag,
    ShoppingCart,
    Tag,
)


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1
    min_num = 1


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeTagInline, RecipeIngredientsInline)
    list_display = ("name", "author", "favorite_recipe")
    list_filter = (
        "name",
        "author",
        "tags",
    )
    search_fields = ("name", "author__username", "tags__name")

    def favorite_recipe(self, obj):
        return obj.favorite_recipe.all().count()


class IngridientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)
    search_fields = ("name",)


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


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    list_filter = ("user", "recipe")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingridient, IngridientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
