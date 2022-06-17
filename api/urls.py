from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'messages/<int:friend_id>', views.MessagesView)
router.register('room_messages/<room_id>', views.RoomMsgsView, basename='room_messages')
router.register(r'users', views.UsersView)
router.register(r'monitor', views.MonitorView)

app_name = 'api'
urlpatterns = [
	path('', include(router.urls)),
]


