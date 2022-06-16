from online_users.models import OnlineUserActivity
import datetime


def see_users():
    user_status = OnlineUserActivity.get_user_activities(time_delta=datetime.timedelta(seconds=60))
    return [user.user for user in user_status]