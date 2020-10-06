from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def chat_index(request):
    context = {'user': request.user, 'inrooms': request.user.inroom_set.all()}
    return render(request, 'chat/chat.html', context)


@login_required
def chat_room(request, room_id):
    context = {'user': request.user, 'inrooms': request.user.inroom_set.all()}
    room = ChatRoom.objects.get(id=room_id)
    context['room_id'] = str(room.id)
    members = room.members.all()
    room_name = ''
    for m in members:
        if m.username != request.user.username:
            room_name = m.username
            break
    context['room_name'] = room_name
    context['chat_log'] = room.chat_log
    return render(request, 'chat/chat.html', context)

