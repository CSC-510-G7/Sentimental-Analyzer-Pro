from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    two_fa_method = models.CharField(max_length=20, choices=[('sms', 'SMS'), ('email', 'Email'), ('authenticator', 'Authenticator App')], default='sms')
    opted_out = models.BooleanField(default=False)
    security_pin = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return self.user.username