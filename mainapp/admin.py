from django.contrib import admin
from mainapp import models


@admin.register(models.Goods)
class CustomUserAdmin(admin.ModelAdmin):
    # list_display = ["id", "username", "email", "is_active", "date_joined"]
    ordering = ["-created_at"]
