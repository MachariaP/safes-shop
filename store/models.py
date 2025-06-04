from django.db import models
from django.urls import reverse

# Create your models here.
class SafeProduct(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='safes/')
    ivory_color = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class ProductSpecification(models.Model):
    product = models.ForeignKey(SafeProduct, related_name='specifications',
                                on_delete=models.CASCADE)
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
