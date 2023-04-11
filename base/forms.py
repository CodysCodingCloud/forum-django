from django.forms import ModelForm
from .models import Room
from django.contrib.auth.forms import UserCreationForm


# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        # fields = ['name']
        fields = '__all__'
