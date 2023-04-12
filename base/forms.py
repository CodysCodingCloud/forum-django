from django.forms import ModelForm
from .models import Room
from django.contrib.auth.forms import UserCreationForm


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
