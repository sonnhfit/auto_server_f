from django.shortcuts import render
from .models import AccountFacebook

def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    list_acount = AccountFacebook.objects.all()
    return render(request, 'chat/index.html', {
        'room_name': room_name, 'list_acount': list_acount
    })
