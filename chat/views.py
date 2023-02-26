from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message, GroupMessage, Room
from chat.serializers import MessageSerializer, UserSerializer, GroupSerializer, RoomSerializer
from django.contrib import messages

def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.error(request,'Username/Password combination incorrect!')
            return redirect('index')
        return redirect('chats')

@csrf_exempt
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            #serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def register_view(request):
    """
    Render registration template
    """
    if request.user.is_authenticated:
        return redirect('chats')
    return render(request, 'chat/register.html', {})


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username),
                       'rooms': Room.objects.all()})

@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'rooms': Room.objects.all(),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})

@csrf_exempt
def room_list(request, pk=None):
    if request.method == 'GET':
        if pk:
            rooms = Room.objects.filter(id=pk)
        else:
            rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def gchat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'rooms': Room.objects.all()})

@csrf_exempt
def gmessage_list(request, sender=None, room=None):
    if request.method == 'GET':
        gmessages = GroupMessage.objects.filter(room_id=room, is_read=False)
        gserializer = GroupSerializer(gmessages, many=True, context={'request': request})
        for gmessage in gmessages:
            gmessage.is_read = True
            gmessage.save()
        return JsonResponse(gserializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        gserializer = GroupSerializer(data=data)
        if gserializer.is_valid():
            gserializer.save()
            return JsonResponse(gserializer.data, status=201)
        return JsonResponse(gserializer.errors, status=400)

def gmessage_view(request, sender, room):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/group.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'rooms': Room.objects.all(),
                       'receiver': Room.objects.get(id=room),
                       'gmessages': GroupMessage.objects.filter(room_id=room)})