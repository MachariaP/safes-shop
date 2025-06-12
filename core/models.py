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
