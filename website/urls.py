from django.urls import path
from . import views


app_name = 'website'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('monitor', views.MonitorView.as_view(), name='monitor'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('signup', views.SignupView.as_view(), name='signup'),

    ]






