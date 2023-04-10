from django.contrib import admin
from mainapp import models


@admin.register(models.Product)
@admin.register(models.BasketItem)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(models.Comment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ["author", "post", "text"]
