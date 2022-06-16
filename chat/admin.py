from django.contrib import admin
from .models import Message, Room, FriendList

admin.site.register(Message)
admin.site.register(Room)
admin.site.register(FriendList)
