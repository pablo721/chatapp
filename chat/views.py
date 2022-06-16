import datetime
from itertools import chain

from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .models import Message, Room, FriendList
from .forms import CreateRoomForm, FindUsersForm
from .utils import see_users


class ChatView(TemplateView):
    template_name = 'chat/chat.html'
    find_users_form = FindUsersForm
    create_room_form = CreateRoomForm




    def post(self, request, *args, **kwargs):
        if 'add_friend' in str(request.POST):
            friend = User.objects.get(id=request.POST['add_friend'])
            friendlist = FriendList.objects.get(user=self.request.user)
            if friend not in friendlist.friends.all():
                friendlist.friends.add(friend)
                friendlist.save()

            return HttpResponseRedirect(reverse('chat:chat'))

    def get_context_data(self, *args, **kwargs):

        user = self.request.user
        users_online = see_users()
        friends = user.user_friends.all().values()
        for friend in friends:
            user = User.objects.get(id=friend['user_id'])
            friend['name'] = user.username
            friend['online'] = user in users_online

        print(friends)
        friend = None
        room = None
        rooms = user.user_rooms.all()
        print(self.request.GET)

        search_results = []
        if 'name' in str(self.request.GET):
            find_form = FindUsersForm(self.request.GET)
            if find_form.is_valid():
                form_data = find_form.cleaned_data
                search_results = User.objects.filter(username__icontains=form_data['name'])
            else:
                print(f'Errors: {find_form.errors}')
        return {'friends': friends, 'rooms': rooms, 'online_users': users_online,
                'create_room_form': self.create_room_form, 'find_friends_form': self.find_users_form,
                'search_results': search_results}


class RoomView(ChatView):

    def get_context_data(self, room_id, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = Room.objects.get(id=room_id)
        return context

    def post(self, request, *args, **kwargs):
        pass


class ChatWithFriendView(ChatView):

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, friend_id, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend'] = User.objects.get(id=friend_id)
        return context



def get_messages(request, friend_id):
    tz_info = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    user = request.user
    recipient = User.objects.get(id=friend_id)
    msgs = []
    sent_msgs = Message.objects.filter(sender=user, recipient=recipient).values()
    msgs.append(sent_msgs)
    if not user == recipient:
        received_msgs = Message.objects.filter(sender=recipient, recipient=user).values()
        msgs.append(received_msgs)

    msgs = sorted(
        chain(*msgs),
        key=lambda instance: instance['timestamp'])

    for msg in msgs:
        if msg['destruct_timer']:
            msg_obj = Message.objects.get(id=msg['id'])
            msg_date = msg['timestamp']
            now = datetime.datetime.now(tz=tz_info)
            delta = (now - msg_date).total_seconds()
            msg['destruct_timer'] = (msg_obj.destruct_timer - delta).__round__(2)
            if delta > msg['destruct_timer']:
                Message.objects.filter(id=msg['id']).delete()
                msgs.remove(msg)

        msg['sender_id'] = User.objects.get(id=msg['sender_id']).username
    return JsonResponse({'messages': msgs})


def send(request):
    print(see_users())
    sender = request.user
    recipient = User.objects.get(id=request.POST['recipient_id'])
    message = request.POST['msg_text']
    date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=1)))
    Message.objects.create(sender=sender, recipient=recipient, content=message, timestamp=date)
    return HttpResponse('message sent')







#old
@login_required
def chat(request, friend_id):
    print('chat2')
    context = {}
    user = request.user
    friends = user.friends.all()
    recipient = MyUser.objects.get(id=friend_id)
    context['profile'] = user
    context['friends'] = friends
    context['recipient'] = recipient
    context['find_users'] = FindUsersForm()
    context['search_results'] = []
    sent_msgs = Message.objects.filter(sender=user, recipient=recipient)
    received_msgs = Message.objects.filter(sender=recipient, recipient=user)
    msgs = sorted(
        chain(sent_msgs, received_msgs),
        key=lambda instance: instance.timestamp)
    context['messages'] = msgs
    return render(request, 'chat/chat.html', context)




@login_required
def messenger(request):
    context = {}
    user = request.user
    friends = user.friends.all()
    context['profile'] = profile
    context['friends'] = friends
    context['recipient'] = None
    context['find_users'] = FindUsersForm()
    context['search_results'] = []
    if request.method == 'GET':
        if 'find_users' in str(request.GET):
            find_form = FindUsersForm(request.GET)
            if find_form.is_valid():
                form_data = find_form.cleaned_data
                name = form_data['name']
                context['search_results'] = MyUser.objects.filter(username__icontains=name)
                print(context['search_results'])
            else:
                print(f'error {find_form.errors}')
    else:
        friend = MyUser.objects.get(user=MyUser.objects.get(id=request.POST['add_friend']))
        if not user.friends.filter(user=friend).exists():
            user.friends.add(friend)
    return render(request, 'chat/chat.html', context)

