from django.contrib import admin

from .models import FoodgramUser


@admin.register(FoodgramUser)
class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'id')
    list_filter = ('email', 'username')
    empty_value_display = '-пусто-'
