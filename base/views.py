""" states and logic for your templates """
from django.shortcuts import render, redirect

# get_object_or_404, get_list_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q, OuterRef, Subquery

# pylint: disable=import-error
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RoomForm, MyUserCreationForm, UserForm
from .models import Room, Topic, Message, User


def login_view(request):
    """login user"""
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except Exception as err:
            print('>>>', err)
            messages.error(request, err)
            messages.error(request, 'User does not exist')
        else:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            messages.error(request, 'Username or Password do not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def register_view(request):
    """registers user using post"""
    page = 'register'
    form = MyUserCreationForm()
    print('user')

    if request.method == 'POST':
        print('POST')
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.username = user.email
            user.save()
            print('valid')
            login(request, user)
            print('login')
            return redirect('/')
        else:
            print('>>>2')
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f'{error}')
            # display error messages
            for message in error_messages:
                messages.error(request, message)
    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


def logout_view(request):
    """logs out user"""
    logout(request)
    return redirect('/')


def home(request):
    """root dir"""
    # queryset = ModelName.objects.all() | get() | filter() | exclude()
    # var      = Mn     q    att    method
    queryset = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=queryset)
        | Q(name__icontains=queryset)
        | Q(description__icontains=queryset)
    ).order_by('-updated')

    for room in rooms:
        try:
            room.latest_message = room.message_set.latest('created')
        except Message.DoesNotExist:
            room.latest_message = None
    topics = Topic.objects.all()
    room_count = rooms.count()
    recent_messages = Message.objects.all()
    # print(topics)
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'recent_messages': recent_messages,
    }
    return render(request, 'base/home.html', context)


def room_view(request, pk):
    """retrieves many to one relationships - messages to room"""
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    # orders by -descending vs ascending
    participants = room.participants.all().order_by('username')
    print(participants)
    participants_count = participants.count()
    if request.method == "POST":
        message = Message.objects.create(
            body=request.POST.get('body'), user=request.user, room=room
        )
        room.participants.add(request.user)
        # message.save()
        # room.message_set(request.POST)
        return redirect('room', pk=room.id)
    if request.method == "DELETE":
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        "room_messages": room_messages,
        'participants': participants,
        "participants_count": participants_count,
    }
    return render(request, 'base/room.html', context)


# CRUD - Rooms
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     # name=request.POST.get('name')
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('/')
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('/')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # initial form data
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('you are not the user')
    if request.method == 'POST':
        # needs initial data to know what to update
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('/')
        print(request.POST)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    # forms can only use GET | POST requests (idempotent)
    # forms cannot sent DELETE or PUT requests because they are not idempotent
    if request.method == 'POST':
        room.delete()
        return redirect('/')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('not the owner')
    if request.method == 'POST':
        message.delete()
        return redirect('/room/' + str(message.room.id))
    return render(request, 'base/delete.html', {'obj': message})


def user_profile(request, pk):
    userinfo = User.objects.get(id=pk)
    rooms = userinfo.room_set.all().filter(host__id=pk).order_by('-created')

    for room in rooms:
        try:
            room.latest_message = room.message_set.latest('created')
        except Exception as err:
            room.latest_message = None
    topics = Topic.objects.all()
    room_count = rooms.count()

    topics = Topic.objects.all()
    recent_messages = userinfo.message_set.all().order_by('-created')
    context = {
        'userinfo': userinfo,
        'rooms': rooms,
        'topics': topics,
        'recent_messages': recent_messages,
    }
    return render(request, 'base/profile.html', context)


from .forms import UserForm


@login_required(login_url='login')
def update_user(request):
    userinfo = request.user
    form = UserForm(instance=userinfo)
    context = {
        # 'userinfo': userinfo,
        'form': form
    }
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=userinfo)
        print(request.POST)
        if form.is_valid():
            print('valid')
            form.save()
            return redirect('user', pk=userinfo.id)
    return render(request, 'base/update_user.html', context)


def room4(request):
    return HttpResponse('room4')


def topics_page(request):
    """just topics page"""
    queryset = (
        request.GET.get('qtopics') if request.GET.get('qtopics') is not None else ''
    )
    topics = Topic.objects.filter(
        Q(name__icontains=queryset)
        # | Q(room__name__icontains=queryset)
        # | Q(room__description__icontains=queryset)
    ).order_by('-updated')
    context = {"topics": topics}
    return render(request, 'base/topics.html', context)


def activities_page(request, pk=None):
    """just feed page"""

    recent_messages = None
    title = "Recent Activiy"
    if pk is not None:
        if str(request.user.id) == pk:
            title = 'My recent Activity'
        else:
            title = str(User.objects.get(id=pk)) + "'s Recent Activity"
        recent_messages = Message.objects.filter(user_id=pk).order_by('-updated')
    else:
        recent_messages = Message.objects.all().order_by('-updated')
    context = {"recent_messages": recent_messages, "title": title}
    return render(request, 'base/activity_page.html', context)


import datetime
from django.db.models.functions import Lower


def myNotes(request, pk):
    instance = Topic.objects.get(pk=1)
    instance.name = 'new description'
    #  ManyToManyField
    instance.participants.add('one', 'two')
    instance.save()

    queryset = Room.objects.all()
    queryset_filter = Room.objects.filter(created=datetime.date.today())
    queryset_exclude = Room.objects.exclude(created__lte=datetime.date(2005, 1, 30))
    queryset.filter(name__startswith="Do")
    queryset.filter(name__iexact="Doctor Who")
    # limit 5
    queryset[:5]
    # off set 5 limit 5
    queryset[5:10]
    # get returns single instance, returns newest
    queryset.order_by('-updated').get()
    queryset.order_by(Lower("name").desc()).get()
    queryset.filter(user__name__contains="Lennon")
    # joins
    queryset_j = Room.objects.filter(blog__name="Beatles Blog")
    # One-to-many relationships
    has_fkey = Room.objects.get(id=2)
    has_fkey.Topic  # access to topic
    target_relationship = Topic.objects.all().room_set.all()
    # Many Many Relationships
    has_ManyToManyField = Room.objects.get(id=5).room_set.all()
    target_of_has_ManyToManyField = Topic.objects.get(id=5)
    populated = target_of_has_ManyToManyField.participants.all()
    populated.count()  # or filter or whatever you fancy
    # One-to-one relationships | works the same on reverse
    has_OneToOneField = User.objects.get(pk=pk)
    has_OneToOneField.profile
    #
    context = {'instance': instance}
    return render(request, '.html', context)
