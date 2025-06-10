from django.contrib import admin
from .models import SafeProduct, StoreLocation, ProductSpecification


class SafeProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    class Media:
        css = {
            'all': ('/static/css/ckeditor.css',)
            
        }

    def description_preview(self, obj):
        return obj.description
    description_preview.allow_tags = True

admin.site.register(SafeProduct, SafeProductAdmin)
admin.site.register(StoreLocation)
admin.site.register(ProductSpecification)
