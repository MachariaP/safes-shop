from django.contrib import admin
from django.utils.html import format_html
from .models import SafeProduct, ProductSpecification, StoreLocation, WishlistItem, Order, OrderItem

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 4
    fields = ('name', 'value', 'icon')
    ordering = ('name',)

@admin.register(SafeProduct)
class SafeProductAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'category', 'price', 'is_in_stock', 'formatted_created_at', 'is_expensive')
    list_filter = ('category', 'is_in_stock', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSpecificationInline]
    list_per_page = 25
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Image')
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 4px;" />', obj.image.url)
        return "-"

    @admin.display(description='Created At')
    def formatted_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")

    @admin.display(description='Expensive?', boolean=True)
    def is_expensive(self, obj):
        return obj.price > 100

    def get_row_css(self, obj):
        return 'high-priority' if obj.price > 100 else ''

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value', 'icon')
    list_filter = ('name',)
    search_fields = ('product__name', 'name', 'value')
    list_select_related = ('product',)
    list_per_page = 25

@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'is_primary', 'phone', 'email')
    search_fields = ('name', 'address', 'phone', 'email')
    list_filter = ('is_primary',)
    list_per_page = 25

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'formatted_added_at')
    search_fields = ('product__name', 'user__username')
    list_select_related = ('product', 'user')
    list_per_page = 25
    ordering = ('-added_at',)

    @admin.display(description='Added At')
    def formatted_added_at(self, obj):
        return obj.added_at.strftime("%Y-%m-%d %H:%M")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_price', 'payment_method', 'is_paid', 'formatted_created_at')
    list_filter = ('payment_method', 'is_paid', 'created_at')
    search_fields = ('order_number', 'contact_email', 'contact_phone')
    list_select_related = ('user',)
    list_per_page = 25
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Created At')
    def formatted_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__order_number', 'product__name')
    list_select_related = ('order', 'product')
    list_per_page = 25
