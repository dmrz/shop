from django.contrib import admin

from .models import Cart


class CartProductInline(admin.TabularInline):
    model = Cart.products.through


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartProductInline]
