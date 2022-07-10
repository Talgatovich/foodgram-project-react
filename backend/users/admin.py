from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "username")
    list_filter = ("first_name", "email")
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
