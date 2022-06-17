from chat.models import Message, Profile
from django.contrib.auth.models import User
import datetime


def delete_messages(user_id):
	tz_info = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
	user = Profile.objects.get(id=user_id)
	sent_msgs = Message.objects.filter(sender=user).values()
	recvd_msgs = Message.objects.filter(recipient=user).values()

	for msg in sent_msgs.union(recvd_msgs):

		if msg['destruct_timer']:
			msg_date = msg['timestamp']
			now = datetime.datetime.now(tz=tz_info)
			delta = (now - msg_date).total_seconds()

			if msg['destruct_timer'] < delta:
				print(f'deletin {msg}')
				Message.objects.get(id=msg['id']).delete()




