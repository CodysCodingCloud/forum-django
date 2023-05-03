from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room

# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    """
    RoomForm(request.POST).save() == Room.(request.POST).save()
    if Id is defined in instance, it becomes an update
    RoomForm(request.POST, instance = Room.objects.get(id=pk)).save()
    """

    class Meta:
        model = Room
        # fields = ['name']
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
