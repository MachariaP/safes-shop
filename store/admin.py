# store/admin.py

"""Admin configuration for the store app models."""

from django.contrib import admin
from .models import SafeProduct, ProductSpecification, StoreLocation, WishlistItem, Order, OrderItem


class ProductSpecificationInline(admin.TabularInline):
    """Inline admin for ProductSpecification to manage specs within SafeProduct."""
    model = ProductSpecification
    extra = 4  # Provide 4 fields for Dimensions, Weight, Capacity, Fire Class
    fields = ('name', 'value', 'icon')
    ordering = ('name',)


@admin.register(SafeProduct)
class SafeProductAdmin(admin.ModelAdmin):
    """Admin configuration for SafeProduct model."""
    list_display = ('name', 'category', 'price', 'is_in_stock', 'created_at')
    list_filter = ('category', 'is_in_stock')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSpecificationInline]


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    """Admin configuration for ProductSpecification model."""
    list_display = ('product', 'name', 'value', 'icon')
    list_filter = ('name',)
    search_fields = ('product__name', 'name', 'value')


@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    """Admin configuration for StoreLocation model."""
    list_display = ('name', 'address', 'is_primary')
    search_fields = ('name', 'address')


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    """Admin configuration for WishlistItem model."""
    list_display = ('product', 'added_at')
    search_fields = ('product__name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model."""
    list_display = ('order_number', 'user', 'total_price', 'payment_method', 'is_paid', 'created_at')
    list_filter = ('payment_method', 'is_paid')
    search_fields = ('order_number', 'contact_email', 'contact_phone')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin configuration for OrderItem model."""
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__order_number', 'product__name')