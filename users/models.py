from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    referral_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    referral_points = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.email
