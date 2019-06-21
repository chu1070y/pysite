from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import User


def updateform(request):
    user = User.objects.get(id=request.session['authuser']['id'])

    data = {
        'user': user
    }

    return render(request, 'user/updateform.html', data)


def update(request):
    user = User.objects.get(id=request.session['authuser']['id'])
    user.name = request.POST['name']
    user.gender = request.POST['gender']

    if request.POST['password'] is not '':
        user.password = request.POST['password']

    user.save()

    request.session['authuser']['name'] = user.name

    return HttpResponseRedirect('/user/updateform?result=success')


def loginform(request):
    return render(request, 'user/loginform.html')


def login(request):
    result = User.objects.filter(email=request.POST['email']).filter(password=request.POST['password'])

    # 로그인 실패
    if len(result) == 0:
        return HttpResponseRedirect('/user/loginform?result=fail')

    # 로그인 성공
    authuser = result[0]
    request.session['authuser'] = model_to_dict(authuser)
    return HttpResponseRedirect('/')


# def logout(request):
#     del request.session['authuser']
#     referer = request.META.get('HTTP_REFERER')
#
#     if not referer:
#         referer = '/'
#
#     return HttpResponseRedirect(referer)

def logout(request):
    del request.session['authuser']
    return HttpResponseRedirect('/')


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


def checkemail(request):
    try:
        user = User.objects.get(email=request.GET['email'])

    except Exception as e:
        user = None

    result = {
        'result': 'success',
        'data': 'not exists' if user is None else 'exists'
    }

    return JsonResponse(result)
