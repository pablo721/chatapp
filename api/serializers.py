from rest_framework import serializers
from chat.models import Message
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ['sender', 'recipient', 'content', 'timestamp', 'delivered', 'read', 'destruct_timer']

