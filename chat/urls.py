from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


app_name = 'chat'
urlpatterns = [
    path('', login_required(views.ChatView.as_view()), name='chat'),
    path('chat/<int:friend_id>', login_required(views.ChatWithFriendView.as_view()), name='chat_with_friend'),
    path('room/<int:room_id>', login_required(views.RoomView.as_view()), name='room'),
 #   path('getMessages/<int:friend_id>', views.get_messages, name='getMessages'),
#    path('addFriend/<int:friend_id>', views.add_friend, name='addFriend'),
    path('send', views.send, name='send'),
    ]



