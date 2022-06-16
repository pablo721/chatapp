from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'messages', views.MessagesView)
router.register(r'users', views.UsersView)
router.register(r'motor', views.MonitorView)

app_name = 'api'
urlpatterns = [
	path('', include(router.urls)),
]


