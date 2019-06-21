from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board
from user.models import User


def board_list(request):
    board = Board.objects.order_by('-groupno', 'orderno')[0:10]

    data = {'boards': board}

    return render(request, 'board/list.html', data)


def board_writeform(request, id=-1):
    data = {"id": id}

    return render(request, 'board/write.html', data)


def board_write(request, id=-1):
    board = Board()

    board.title = request.POST['title']
    board.content = request.POST['content']
    board.user = User.objects.get(id=request.session['authuser']['id'])

    if id != -1:
        row = Board.objects.get(id=id)
        board.groupno = row.groupno
        board.orderno = row.orderno + 1
        board.depth = row.depth + 1

        Board.objects.filter(groupno=row.groupno).filter(orderno__gte=board.orderno).update(orderno=F('orderno') + 1)

        board.save()

        return HttpResponseRedirect('/board/')

    max_groupno = Board.objects.aggregate(max_groupno=Max('groupno'))
    board.groupno = 0 if max_groupno['max_groupno'] is None else max_groupno['max_groupno'] + 1

    board.save()

    return HttpResponseRedirect('/board/')


def board_view(request, id=0):
    board = Board.objects.get(id=id)

    data = {"board": board}

    return render(request, 'board/view.html', data)


def board_delete(request, id=0):
    row = Board.objects.get(id=id)
    row.remove = 1
    row.save()

    return HttpResponseRedirect('/board/')


def board_modifyform(request, id=0):
    board = Board.objects.get(id=id)

    data = {"board": board}

    return render(request, 'board/modify.html', data)


def board_modify(request, id=0):
    row = Board.objects.get(id=id)
    row.title = request.POST['title'] if request.POST['title'] != '' else Board.objects.get(id=id).title
    row.content = request.POST['content']
    row.save()

    return HttpResponseRedirect('/board/' + str(id))
