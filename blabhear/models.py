import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=150, blank=True)
    display_name = models.CharField(max_length=150, blank=True)

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.username
        super(User, self).save(*args, **kwargs)
