from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls'), name='chat'),
    path('api/', include('api.urls'), name='api'),
    path('', include('website.urls'), name='index')
]


