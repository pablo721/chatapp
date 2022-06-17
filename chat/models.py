from django.db import models
import datetime


class Profile(models.Model):
	user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='user_profile')

	messages = models.ManyToManyField('chat.Message', related_name='user_messages', blank=True)
	rooms = models.ManyToManyField('chat.Room', related_name='user_rooms', blank=True)
	friends = models.ManyToManyField('self', blank=True)

	def __str__(self):
		return self.user.get_username()


class Message(models.Model):
	sender = models.ForeignKey('chat.Profile', on_delete=models.CASCADE, unique=False, related_name='message_sender',
							    blank=True)
	recipient = models.ForeignKey('chat.Profile', on_delete=models.CASCADE, unique=False, default=1,
								   related_name='message_recipient', blank=True)
	room = models.ForeignKey('chat.Room', on_delete=models.CASCADE, default=1, related_name='message_room', blank=True)
	content = models.TextField(max_length=1000, blank=False)
	timestamp = models.DateTimeField(blank=True)
	delivered = models.BooleanField(default=False)
	read = models.BooleanField(default=False)
	destruct_timer = models.IntegerField(blank=True, null=True, default=50)

	def __str__(self):
		return str(self.timestamp) + ' ' + self.sender.user.get_username() + ': ' + str(self.content)


class Room(models.Model):
	creator = models.ForeignKey('chat.Profile', on_delete=models.CASCADE, related_name='room_creator')
	room_name = models.CharField(max_length=32)
	creation_date = models.DateTimeField()
	private = models.BooleanField(default=False)
	users = models.ManyToManyField('chat.Profile', related_name='room_users', blank=True)






