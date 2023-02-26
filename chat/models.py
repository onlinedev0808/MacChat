from django.contrib.auth.models import User
from django.db import models

class Room(models.Model):
    room = models.CharField(max_length=1200)
    def __str__(self):
        return self.room
    class Meta:
        ordering = ('room',)

class Message(models.Model):
     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
     message = models.CharField(max_length=1200)
     timestamp = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default=False)
     def __str__(self):
           return self.message
     class Meta:
           ordering = ('timestamp',)

class GroupMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_sender')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_id')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return self.message
    class Meta:
        ordering = ('timestamp',)