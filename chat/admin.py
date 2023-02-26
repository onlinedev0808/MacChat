from django.contrib import admin
from chat.models import Message, GroupMessage, Room

admin.site.register(Message)
admin.site.register(GroupMessage)
admin.site.register(Room)