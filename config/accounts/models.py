from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    name = models.CharField(max_length=100)

    phone_no = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    email = models.EmailField(unique=True)

    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

