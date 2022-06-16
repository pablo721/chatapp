from chat.models import Message
from django.contrib.auth.models import User
import datetime


def delete_messages(user_id):
	tz_info = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
	user = User.objects.get(id=user_id)
	sent_msgs = Message.objects.filter(sender=user).values()
	recvd_msgs = Message.objects.filter(recipient=user).values()

	for msg in sent_msgs.union(recvd_msgs):

		if msg['destruct_timer']:
			msg_date = msg['timestamp']
			now = datetime.datetime.now(tz=tz_info)
			delta = (now - msg_date).total_seconds()
			msg_obj = Message.objects.get(id=msg['id'])
			msg_obj.destruct_timer = int(msg['destruct_timer'] - delta)
			msg_obj.save()
			if msg_obj.destruct_timer <= 0:
				print(f'deletin {msg_obj}')
				msg_obj.delete()



def delete_for_all_users():
	for user in User.objects.all():
		delete_messages()


