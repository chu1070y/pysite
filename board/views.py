from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board
from board.service import Pageinfo
from user.models import User


def board_list(request):
    page_info = Pageinfo()
    page = 1
    print("---------------12121")

    if request.method == 'GET':
        print("---------------2222")
        try:
            print(request.GET['page'])
            page = int(request.GET['page'])
        except Exception:
            pass

    elif request.method == 'POST':
        print("---------------333")
        try:
            page = int(request.POST['page'])
        except Exception:
            pass

    page_info.set_page(page)
    page_info.set_total_count(Board.objects.count())

    board = Board.objects.order_by('-groupno', 'orderno')[page_info.start:page_info.start + page_info.display]

    data = {'boards': board, "page_info": page_info}

    return render(request, 'board/list.html', data)


def board_writeform(request, id=-1):
    try:
        page = request.GET['page']
    except Exception:
        page = 1

    data = {"id": id, "page": page}

    return render(request, 'board/write.html', data)


def board_write(request, id=-1):
    try:
        page = request.POST['page']
    except Exception:
        page = 1

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

        return HttpResponseRedirect('/board?page=' + str(page))

    max_groupno = Board.objects.aggregate(max_groupno=Max('groupno'))
    board.groupno = 0 if max_groupno['max_groupno'] is None else max_groupno['max_groupno'] + 1

    board.save()

    return HttpResponseRedirect('/board?page=' + str(page))


def board_view(request, id=0):
    board = Board.objects.get(id=id)

    try:
        page = request.GET['page']
    except Exception:
        page = 1

    data = {"board": board, "page": page}

    return render(request, 'board/view.html', data)


def board_delete(request, id=0):
    row = Board.objects.get(id=id)
    row.remove = 1
    row.save()

    try:
        page = request.GET['page']
    except Exception:
        page = 1

    return HttpResponseRedirect('/board?page=' + str(page))


def board_modifyform(request, id=0):
    board = Board.objects.get(id=id)

    try:
        page = request.GET['page']
    except Exception:
        page = 1

    data = {"board": board, "page": page}

    return render(request, 'board/modify.html', data)


def board_modify(request, id=0):
    row = Board.objects.get(id=id)
    row.title = request.POST['title'] if request.POST['title'] != '' else Board.objects.get(id=id).title
    row.content = request.POST['content']
    row.save()

    try:
        page = request.POST['page']
    except Exception:
        page = 1

    return HttpResponseRedirect('/board/' + str(id) + "?page=" + str(page))
