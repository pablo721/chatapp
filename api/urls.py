from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'messages', views.MessagesView, basename='messages')
router.register('room_messages', views.RoomMsgsView, basename='room_messages')
router.register(r'users', views.UsersView)
router.register(r'monitor', views.MonitorView)

app_name = 'api'
urlpatterns = [
	path('', include(router.urls)),
]


