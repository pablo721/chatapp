import datetime
from itertools import chain
from django.shortcuts import render
import django_filters.rest_framework as rest_filters
from rest_framework import viewsets, filters, generics
from django.contrib.auth.models import User
from django.http import JsonResponse
from .serializers import *
from chat.models import *
from .utils import delete_messages


class MonitorView(viewsets.ModelViewSet):
	queryset = Message.objects.all()
	serializer_class = MessageSerializer


class UsersView(viewsets.ModelViewSet):
	queryset = User.objects.all()


class RoomsView(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	filter_backends = [rest_filters.DjangoFilterBackend]

	def get_queryset(self):
		rooms = Room.objects.filter(private=False)


class RoomMsgsView(viewsets.ModelViewSet):
	queryset = Message.objects.all()
	serializer_class = MessageSerializer
	filter_backends = [rest_filters.DjangoFilterBackend]

	def get_queryset(self):
		print(str(self.request))
		#room = Room.objects.get(id=room_id)





class MessagesView(viewsets.ModelViewSet):

	queryset = Message.objects.all()
	serializer_class = MessageSerializer
	filter_backends = [rest_filters.DjangoFilterBackend]

	def get_queryset(self):
		print(self.request.GET)
		user = Profile.objects.get(user=self.request.user)
		delete_messages(user.id)
		friend = Profile.objects.get(id=self.request.GET['friend_id'])
		sent_msgs = Message.objects.filter(sender=user, recipient=friend).values()
		received_msgs = Message.objects.filter(sender=friend, recipient=user).values()
		msgs = sent_msgs.union(received_msgs).order_by('timestamp')
		for msg in msgs:
			msg['sender_id'] = User.objects.get(id=msg['sender_id']).username
			if msg['destruct_timer']:
				tz_info = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
				msg_date = msg['timestamp']
				now = datetime.datetime.now(tz=tz_info)
				delta = (now - msg_date).total_seconds()
				msg['destruct_timer'] = msg['destruct_timer'] - delta
		return msgs


