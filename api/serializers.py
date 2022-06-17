from rest_framework import serializers
from chat.models import Message, Room, Profile
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ['sender_id', 'recipient', 'content', 'timestamp', 'delivered', 'read', 'destruct_timer']


class RoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = ['room_name', 'creator', 'users', 'private', 'creation_date']


class RoomMsgSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ['sender_id', 'room_id', 'content', 'timestamp', 'delivered', 'read', 'destruct_timer']

