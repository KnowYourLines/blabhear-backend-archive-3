import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=150, blank=True)
    display_name = models.CharField(max_length=150, blank=True)

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.username
        super(User, self).save(*args, **kwargs)


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(User)
    private = models.BooleanField(blank=False, default=False)
    display_name = models.CharField(max_length=150, blank=True)

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.id
        super(Room, self).save(*args, **kwargs)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        other_messages = Message.objects.filter(
            room=self.room, creator=self.creator
        ).exclude(id=self.id)
        if other_messages.exists():
            raise ValidationError(_("Message must be unique per creator in room."))
        super(Message, self).save(*args, **kwargs)


class JoinRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        other_requests = JoinRequest.objects.filter(
            user=self.user, room=self.room
        ).exclude(id=self.id)
        if other_requests.exists():
            raise ValidationError(_("Join request must be unique per user in room."))
        super(JoinRequest, self).save(*args, **kwargs)


class UserNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)
    message = models.ForeignKey(
        Message, blank=True, null=True, on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        other_notifications = UserNotification.objects.filter(
            user=self.user, room=self.room
        ).exclude(id=self.id)
        if other_notifications.exists():
            raise ValidationError(
                _("User notification must be unique per user in room.")
            )
        super(UserNotification, self).save(*args, **kwargs)
