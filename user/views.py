from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from user.models import User


def loginform(request):
    return render(request, 'user/loginform.html')


def login(request):
    email = request.POST['email']
    password = request.POST['password']

    user = User.objects.filter(email=email).filter(password=password)

    if len(user) == 1:
        data = {"user": user}
        return HttpResponseRedirect('/', data)

    return HttpResponseRedirect('/user/loginform')


def joinform(request):
    return render(request, 'user/joinform.html')


def join(request):
    user = User()

    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']

    user.save()

    return HttpResponseRedirect('/user/joinsuccess')


def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')
