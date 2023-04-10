from django.contrib import admin
from mainapp import models


@admin.register(models.Product)
# @admin.register(models.ProductFeedback)
@admin.register(models.BasketItem)
class CustomUserAdmin(admin.ModelAdmin):
    # list_display = ["id", "username", "email", "is_active", "date_joined"]
    # ordering = ["-created_at"]
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(models.ProductFeedback)
class ProductFeedbackAdmin(admin.ModelAdmin):
    list_display = ["rating", "product", "user", ]
