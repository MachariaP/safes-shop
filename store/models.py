from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from ckeditor.fields import RichTextField
import uuid

class SafeProduct(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = RichTextField()
    is_in_stock = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='safes/', null=True, blank=True)
    ivory_color = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=50, choices=[
        ('home', 'Home/Commercial'),
        ('cabinet', 'Cabinet'),
        ('wall', 'Wall'),
    ], default='home')

    class Meta:
        ordering = ['name']

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
    product = models.ForeignKey(SafeProduct, related_name='specifications', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} : {self.value}"

class CartItem(models.Model):
    product = models.ForeignKey(SafeProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} * {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price

class WishlistItem(models.Model):
    product = models.ForeignKey(SafeProduct, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in Wishlist"

class StoreLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    google_map_url = models.URLField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    is_primary = models.BooleanField(default=False)

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
        related_name='orders'
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)
    order_number = models.CharField(max_length=32, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    is_paid = models.BooleanField(default=False)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    checkout_request_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.order_number or 'Pending'}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def _generate_order_number(self):
        return f"ORD-{uuid.uuid4().hex[:10].upper()}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(SafeProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
