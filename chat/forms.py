from django import forms



class FindUsersForm(forms.Form):
    name = forms.CharField(label='Username', max_length=32,
                           widget=forms.TextInput(attrs={'placeholder': 'Find users/rooms'}))


class CreateRoomForm(forms.Form):
    room_name = forms.CharField(max_length=16, label='Create room', widget=forms.TextInput(attrs={'placeholder': 'Room name..'}))
    private = forms.BooleanField(required=False)
