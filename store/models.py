from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.
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
        ('home_commercial', 'Home/Commercial'),
        ('cabinet', 'Cabinet'),
        ('wall', 'Wall'),
    ], default='home_commercial')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)  # Converts to lowercase by default
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

class StoreLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    google_map_url = models.URLField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.name
