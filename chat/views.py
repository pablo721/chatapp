import datetime
from itertools import chain

from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .models import Message, Room, Profile
from .forms import CreateRoomForm, FindUsersForm
from .utils import see_users, clear_history


class ChatView(TemplateView):
    template_name = 'chat/chat.html'
    find_users_form = FindUsersForm
    create_room_form = CreateRoomForm

    def post(self, request, *args, **kwargs):
        user = Profile.objects.get(user=request.user)
        if 'add_friend' in str(request.POST):
            friend = Profile.objects.get(user=User.objects.get(id=request.POST['add_friend']))
            if friend not in user.friends.all():
                user.friends.add(friend)
                user.save()
                return HttpResponseRedirect(reverse('chat:chat_with_friend', args=(friend.id,)))
        return HttpResponseRedirect(reverse('chat:chat'))

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        profile = user.user_profile
        users_online = see_users()
        friends = [(f.user.username, f.id, f.user in users_online) for f in profile.friends.all()]
        friend = None
        room = None
        owned_rooms = Room.objects.filter(creator=profile)
        priv_rooms = profile.rooms.all()
        pub_rooms = Room.objects.filter(private=False)
        rooms = owned_rooms.union(priv_rooms, pub_rooms)



        search_results = []
        if 'name' in str(self.request.GET):
            find_form = FindUsersForm(self.request.GET)
            if find_form.is_valid():
                form_data = find_form.cleaned_data
                search_results = User.objects.filter(username__icontains=form_data['name'])
            else:
                print(f'Errors: {find_form.errors}')
        return {'friend': friend, 'friends': friends, 'pub_rooms': pub_rooms, 'rooms': rooms,
                'priv_rooms': priv_rooms, 'owned_rooms': owned_rooms, 'room': room, 'online_users': users_online,
                'create_room_form': self.create_room_form, 'find_friends_form': self.find_users_form,
                'search_results': search_results}


class ChatWithFriendView(ChatView):

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(kwargs)
        user = Profile.objects.get(user=request.user)
        friend = Profile.objects.get(id=kwargs['friend_id'])
        if 'clear_history' in str(request.POST):
            clear_history(user.id, friend.id)

        elif 'msg_text' in str(request.POST):
            print(f'msg \n {request.POST}')
            date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=1)))
            Message.objects.create(sender=user, recipient=friend, content=request.POST['msg_text'],
                                   timestamp=date)
            #destruct_timer=request.POST['destr_timer']

        return HttpResponseRedirect(reverse('chat:chat_with_friend', args=(friend.id,)))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend'] = Profile.objects.get(id=kwargs['friend_id'])
        return context


class RoomView(ChatView):
    model = Room
    create_room_form = CreateRoomForm


    def get_context_data(self, room_id, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(id=room_id)
        context['room'] = room
        context['messages'] = Message.objects.filter(room=room)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'join_room_btn' in str(request.POST):
            room = Room.objects.get(id=request.POST['join_room_btn'])
            profile = Profile.objects.get(user=request.user)
            profile.rooms.add(room)
            profile.save()

        return HttpResponseRedirect(reverse('chat:room', args=(context['room'].id, )))



def delete_friend(request):
    user = Profile.objects.get(user=request.user)
    if request.method == "POST" and 'del_friend_btn' in str(request.POST):
        friend = Profile.objects.get(id=request.POST['del_friend_btn'])
        if friend in user.friends.all():
            user.friends.remove(friend)
            user.save()
        return HttpResponseRedirect(reverse('chat:chat'))


def add_friend(request):
    if request.method == "POST" and 'add_friend' in str(request.POST):
        user = Profile.objects.get(user=request.user)
        friend = Profile.objects.get(user=User.objects.get(id=request.POST['add_friend']))
        if friend not in user.friends.all():
            user.friends.add(friend)
        return HttpResponseRedirect(reverse('chat:chat'))


def create_room(request):
    if request.method == "POST":
        room_form = CreateRoomForm(request.POST)
        if room_form.is_valid():
            form_data = room_form.cleaned_data
            form_data['creator'] = request.user.user_profile
            form_data['creation_date'] = datetime.datetime.now(datetime.timezone.utc)
            r = Room.objects.create(**form_data)
        else:
            print(f'errors: {room_form.errors}')

        return HttpResponseRedirect(reverse('chat:room', args=(r.id, )))



def send(request):
    sender = Profile.objects.get(user=request.user)
    message = request.POST['msg_text']
    destr_timer = request.POST['destr_timer']
    date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=1)))
    if 'friend_id' in str(request.POST):
        recipient = Profile.objects.get(id=request.POST['recipient_id'])
        Message.objects.create(sender=sender, recipient=recipient, content=message, timestamp=date,
                               destruct_timer=destr_timer)
        return HttpResponseRedirect(reverse('chat:chat_with_friend', args=(recipient.id,)))
    elif 'room_id' in str(request.POST):
        room = Room.objects.get(id=request.POST['room_id'])
        Message.objects.create(sender=sender, recipient=sender, content=message, timestamp=date, to_room=True,
                               destruct_timer=destr_timer, room=room)
        return HttpResponseRedirect(reverse('chat:room', args=(room.id,)))










#old
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

