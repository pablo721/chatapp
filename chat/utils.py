from online_users.models import OnlineUserActivity
import datetime
from django.contrib.auth.models import User
from .models import Message, Profile, Room, Friendship


def see_users():
	user_status = OnlineUserActivity.get_user_activities(time_delta=datetime.timedelta(seconds=60))
	return [user.user for user in user_status]


def clear_history(user_id, friend_id):
	user = Profile.objects.get(id=user_id)
	friend = Profile.objects.get(id=friend_id)
	Message.objects.filter(sender=user).filter(recipient=friend).delete()
	if not user_id == friend_id:
		Message.objects.filter(sender=friend).filter(recipient=user).delete()

