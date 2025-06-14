from django.db import models

# Create your models here.
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True, help_text="Short description of the team member")
    image = models.ImageField(upload_to='team/', default='team/default.jpg', blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Order for display (lower number first)")
    is_active = models.BooleanField(default=True, help_text="Show this team member on the website")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} ({self.title})"

class Solution(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Used in URLs, e.g., 'home-security'")
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class, e.g., 'fas fa-home'")
    description = models.TextField()
    features = models.JSONField(help_text="List of features, e.g., ['Feature 1', 'Feature 2']")
    order = models.PositiveIntegerField(default=0, help_text="Order of display")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, help_text="Job title or position")
    quote = models.TextField()
    rating = models.FloatField(default=5.0, help_text="Rating out of 5, e.g., 4.5")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.title}"