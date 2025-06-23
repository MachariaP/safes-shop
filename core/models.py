from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class TeamMember(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True)  # Indexed for search
    title = models.CharField(max_length=100,
                             db_index=True)  # Indexed for search and filter
    bio = models.TextField(max_length=500,
                           blank=True,
                           help_text="Short description of the team member")
    image = models.ImageField(upload_to='team/',
                              default='team/default.jpg',
                              blank=True)
    order = models.PositiveIntegerField(default=0,
                                        help_text="Order for display (lower\
                                        number first)",
                                        db_index=True)  # Indexed for ordering
    is_active = models.BooleanField(default=True,
                                    help_text="Show this team member\
                                    on the website",
                                    db_index=True)  # Indexed for filter

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        indexes = [
            models.Index(fields=['name', 'title']),
            models.Index(fields=['order', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.title})"


class Solution(models.Model):
    title = models.CharField(max_length=100,
                             db_index=True)  # Indexed for search
    slug = models.SlugField(unique=True, help_text="Used in URLs, e.g.,\
                            'home-security'")
    icon = models.CharField(max_length=50,
                            help_text="Font Awesome icon class, e.g.,\
                            'fas fa-home'")
    description = models.TextField()
    features = models.TextField(help_text="JSON-like string of features, e.g.,\
                                '[\"Feature 1\", \"Feature 2\"]'")
    order = models.PositiveIntegerField(default=0,
                                        help_text="Order of display",
                                        db_index=True)  # Indexed for ordering
    created_at = models.DateTimeField(auto_now_add=True,
                                      db_index=True)  # Indexed for filter

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['title', 'created_at']),
        ]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True)  # Indexed for search
    title = models.CharField(max_length=100,
                             help_text="Job title or position",
                             db_index=True)  # Indexed for search
    quote = models.TextField()
    rating = models.FloatField(default=5.0,
                               help_text="Rating out of 5, e.g., 4.5",
                               db_index=True)  # Indexed for filter
    created_at = models.DateTimeField(auto_now_add=True,
                                      db_index=True)  # Indexed for filter

    class Meta:
        indexes = [
            models.Index(fields=['name', 'title', 'rating']),
        ]

    def __str__(self):
        return f"{self.name} - {self.title}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        db_index=True  # Indexed for ForeignKey
    )
    phone = models.CharField(max_length=20, blank=True, null=True,
                             db_index=True)  # Indexed for search
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.get_or_create(user=instance)
