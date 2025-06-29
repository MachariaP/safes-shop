from django.contrib import admin
from django.utils.html import format_html
from .models import TeamMember, Solution, Testimonial, Profile


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('title', 'is_active')
    search_fields = ('name', 'title')
    list_per_page = 25
    ordering = ('order', 'name')
    readonly_fields = ('image_preview',)
    fields = ('name', 'title', 'bio', 'image', 'image_preview',
              'order', 'is_active')

    @admin.display(description='Image')
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50"\
                               style="border-radius: 4px;" />', obj.image.url)
        return "-"

    @admin.display(description='Image Preview')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" />', obj.image.url)
        return "-"


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'formatted_created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    list_per_page = 25
    ordering = ('order',)
    readonly_fields = ('created_at',)

    @admin.display(description='Created At')
    def formatted_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'rating', 'formatted_created_at',
                    'highlight_rating')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'title', 'quote')
    list_per_page = 25
    readonly_fields = ('created_at',)

    @admin.display(description='Created At')
    def formatted_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")

    @admin.display(description='High Rating', boolean=True)
    def highlight_rating(self, obj):
        return obj.rating >= 4.5

    def get_row_css(self, obj):
        return 'high-priority' if obj.rating >= 4.5 else ''


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'formatted_updated_at')
    list_select_related = ('user',)  # Optimize ForeignKey query
    search_fields = ('user__username', 'phone')
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Updated At')
    def formatted_updated_at(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d %H:%M")
