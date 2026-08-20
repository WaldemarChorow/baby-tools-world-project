"""Django admin configuration for products app.

This module registers models with the Django admin interface and configures
their display, filtering, and search options.
"""

from django.contrib import admin

from .models import Category, Comment, Product, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "average_rating", "rating_count", "created_at")
    list_select_related = ("category",)
    list_filter = ("tags",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "guest_name", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("guest_name", "guest_email", "text", "user__username")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for Tag model.

    Provides list display and search functionality for managing product tags.
    """

    list_display = ("name", "created_at")
    search_fields = ("name",)
