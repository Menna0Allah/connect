from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RoomForm
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    ) 
    room_count = rooms.count()
    topics = Topic.objects.all()
    messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    liked_rooms = set()
    if request.user.is_authenticated:
        liked_rooms = set(RoomLike.objects.filter(user=request.user).values_list('room_id', flat=True))
    
    context = {
        'rooms': rooms, 
        'room_count': room_count, 
        'topics': topics, 
        'messages': messages,
        'liked_rooms': liked_rooms,
    }

    return render(request, 'activities/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    liked_rooms = set()
    liked_messages = set()
    if request.user.is_authenticated:
        liked_rooms = set(RoomLike.objects.filter(user=request.user).values_list('room_id', flat=True))
        liked_messages = set(MessageLike.objects.filter(user=request.user).values_list('message_id', flat=True))

    # Query related rooms with the same topic, excluding the current room
    related_rooms = Room.objects.filter(topic=room.topic).exclude(id=pk).order_by('-updated')[:5]

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )

        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'messages': messages, 
        'participants':participants,
        'related_rooms':related_rooms,
        'liked_rooms': liked_rooms,
        'liked_messages': liked_messages,
    }

    return render(request, 'activities/room.html', context)


@login_required(login_url='users:login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user

            new_topic_name = form.cleaned_data['new_topic']
            if new_topic_name:
                topic, created = Topic.objects.get_or_create(name=new_topic_name)
                room.topic = topic
            else:
                room.topic = form.cleaned_data['topic']

            room.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'activities/room_form.html', context)


@login_required(login_url='users:login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
    
        if form.is_valid():
            new_topic_name = form.cleaned_data['new_topic']
            if new_topic_name:
                topic, created = Topic.objects.get_or_create(name=new_topic_name)
                room.topic = topic
            else:
                room.topic = form.cleaned_data['topic']
            form.save()
            return redirect('home')
    
    if request.user != room.host:
        raise PermissionDenied("You can only update your own rooms.")
        
    context = {'form':form}
    return render(request, 'activities/room_form.html', context)


@login_required(login_url='users:login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    if request.user != room.host:
        raise PermissionDenied("You can only update your own rooms.")

    return render(request, 'activities/delete.html', {'obj': room})   


@login_required(login_url='users:login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    if request.user != message.user:
        raise PermissionDenied("You can only update your own messages.")

    return render(request, 'activities/delete.html', {'obj': message})   

# Added: AJAX views for liking/unliking rooms and messages
@login_required(login_url='users:login')
def like_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    liked = RoomLike.objects.filter(user=request.user, room=room).exists()
    
    if liked:
        RoomLike.objects.filter(user=request.user, room=room).delete()
        liked = False
    else:
        RoomLike.objects.create(user=request.user, room=room)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': room.likes.count(),
    })

@login_required(login_url='users:login')
def like_message(request, pk):
    message = get_object_or_404(Message, id=pk)
    liked = MessageLike.objects.filter(user=request.user, message=message).exists()
    
    if liked:
        MessageLike.objects.filter(user=request.user, message=message).delete()
        liked = False
    else:
        MessageLike.objects.create(user=request.user, message=message)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': message.likes.count(),
    })