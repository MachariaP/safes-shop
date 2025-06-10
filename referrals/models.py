from django.conf import settings
from django.db import models

# Create your models here.
class Referral(models.Model):
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='referrals',
                                 on_delete=models.CASCADE)
    referee = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    points_awarder = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer} -> {self.referee}"
