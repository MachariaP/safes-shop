# core/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import TeamMember, Solution, Testimonial

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'title')
    list_filter = ['title', 'is_active']
    fields = ('name', 'title', 'bio', 'image', 'order', 'is_active')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'rating', 'created_at')
    search_fields = ('name', 'title', 'quote')
    list_filter = ('rating', 'created_at')
