from django.db import models
import datetime


class Message(models.Model):
	sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, unique=False, related_name='message_sender',
							    blank=True)
	recipient = models.ForeignKey('auth.User', on_delete=models.CASCADE, unique=False, blank=True,
								   related_name='message_recipient')
	content = models.TextField(max_length=1000, blank=False)
	timestamp = models.DateTimeField()
	delivered = models.BooleanField(default=False)
	read = models.BooleanField(default=False)
	destruct_timer = models.IntegerField(blank=True, null=True, default=50)

	# room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, default=0)

	def __str__(self):
		return str(self.timestamp) + ' ' + self.sender.get_username() + ': ' + str(self.content)


class Room(models.Model):
	name = models.CharField(max_length=32)
	creation_date = models.DateTimeField()
	creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	users = models.ManyToManyField('auth.User', related_name='user_rooms')


class FriendList(models.Model):
	user = models.OneToOneField('auth.User', related_name='user_friendlist', on_delete=models.CASCADE)
	friend = models.ManyToManyField('auth.User', related_name='user_friends')





