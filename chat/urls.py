from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


app_name = 'chat'
urlpatterns = [
    path(r'', login_required(views.ChatView.as_view()), name='chat'),
    path(r'<int:friend_id>', login_required(views.ChatWithFriendView.as_view()), name='chat_with_friend'),
    path(r'room/<int:room_id>', login_required(views.RoomView.as_view()), name='room'),
 #   path('get_messages/<int:friend_id>', views.get_messages, name='get_messages'),
#    path('addFriend/<int:friend_id>', views.add_friend, name='addFriend'),
    path(r'send', login_required(views.send), name='send'),
    path(r'new_room', views.create_room, name='create_room'),
    path(r'add_friend', views.add_friend, name='add_friend'),
    path(r'delete_friend', views.delete_friend, name='delete_friend'),
    ]



