from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def guestbook_list(request):
    guestbook = Guestbook.objects.order_by('-id')
    data = {'guestbooks': guestbook}

    return render(request, 'guestbook/list.html', data)


def guestbook_add(request):
    guestbook = Guestbook()

    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.content = request.POST['content']

    guestbook.save()

    return HttpResponseRedirect('/guestbook')


def guestbook_deleteform(request, id=0):
    data = {'id': id}

    return render(request, 'guestbook/deleteform.html', data)


def guestbook_delete(request):
    guestbook = Guestbook()

    guestbook.id = request.POST['id']
    guestbook.password = request.POST['password']

    row = Guestbook.objects.filter(id=guestbook.id).filter(password=guestbook.password)

    row.delete()

    return HttpResponseRedirect('/guestbook')
