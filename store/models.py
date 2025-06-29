import os
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from ckeditor.fields import RichTextField
import uuid

# Dynamically generate icon choices from static/icons/
ICON_DIR = os.path.join(settings.STATICFILES_DIRS[0], 'icons')
ICON_CHOICES = [(f, f) for f in os.listdir(ICON_DIR) if os.path.isfile(os.path.join(ICON_DIR, f))]

class SafeProduct(models.Model):
    name = models.CharField(max_length=200, db_index=True)  # Indexed for search
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = RichTextField()
    is_in_stock = models.BooleanField(default=True, db_index=True)  # Indexed for filter
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='safes/', null=True, blank=True)
    ivory_color = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Indexed for filter
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=50, choices=[
        ('home', 'Home'),
        ('cabinet', 'Cabinet'),
        ('wall', 'Wall'),
    ], default='home', db_index=True)  # Indexed for filter

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name', 'is_in_stock', 'created_at', 'category']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            while SafeProduct.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})

class ProductSpecification(models.Model):
    product = models.ForeignKey(SafeProduct, related_name='specifications', on_delete=models.CASCADE, db_index=True)  # Indexed for ForeignKey
    name = models.CharField(max_length=100, db_index=True)  # Indexed for filter
    value = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, choices=ICON_CHOICES, blank=True, null=True,
                           help_text="Select an icon from the available options.")

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} : {self.value}"

class WishlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True, null=True, blank=True)  # Indexed for ForeignKey
    product = models.ForeignKey(SafeProduct, on_delete=models.CASCADE, db_index=True)  # Indexed for ForeignKey
    added_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Indexed for ordering

    class Meta:
        indexes = [
            models.Index(fields=['added_at']),
        ]

    def __str__(self):
        return f"{self.product.name} in Wishlist"

class StoreLocation(models.Model):
    name = models.CharField(max_length=100, db_index=True)  # Indexed for search
    address = models.TextField()
    google_map_url = models.URLField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    is_primary = models.BooleanField(default=False, db_index=True)  # Indexed for filter

    class Meta:
        indexes = [
            models.Index(fields=['name', 'is_primary']),
        ]

    def __str__(self):
        return self.name

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('MPESA', 'M-Pesa'),
        ('VISA', 'Visa'),
        ('MASTERCARD', 'Mastercard'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        db_index=True  # Indexed for ForeignKey
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)
    order_number = models.CharField(max_length=32, unique=True, editable=False, db_index=True)  # Indexed for search
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Indexed for filter
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, db_index=True)  # Indexed for filter
    is_paid = models.BooleanField(default=False, db_index=True)  # Indexed for filter
    contact_email = models.EmailField(db_index=True)  # Indexed for search
    contact_phone = models.CharField(max_length=20, db_index=True)  # Indexed for search
    shipping_address = models.TextField()
    checkout_request_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['order_number', 'contact_email', 'contact_phone']),
        ]

    def __str__(self):
        return f"Order #{self.order_number or 'Pending'}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def _generate_order_number(self):
        return f"ORD-{uuid.uuid4().hex[:10].upper()}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, db_index=True)  # Indexed for ForeignKey
    product = models.ForeignKey(SafeProduct, on_delete=models.CASCADE, db_index=True)  # Indexed for ForeignKey
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['order', 'product']),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
