from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board
from board.service import Pageinfo
from user.models import User


# 게시판 리스트
# 검색 기능과 페이징 기능
def board_list(request):
    page_info = Pageinfo()  # 페이징 로직 (service.py)
    page = 1

    # 파라미터 추출 -----------------------
    try:
        kwd = request.GET['kwd']
    except Exception:
        kwd = ''

    try:
        page = int(request.GET['page'])
    except Exception:
        pass
    # --------------------------------------

    # 현재 페이지와 전체 게시글 수로 페이징 정보 계산
    page_info.set_page(page)
    page_info.set_total_count(Board.objects.count())

    # 데이터 추출 - ORM with 페이징 정보, 검색
    board = Board.objects.filter(title__icontains=kwd).order_by('-groupno', 'orderno')[
            page_info.start:page_info.start + page_info.display]

    # 게시판 정보와 페이징 정보 dict 형태로 합치기
    data = {'boards': board, "page_info": page_info}

    return render(request, 'board/list.html', data)


# 게시판 글쓰기 양식
def board_writeform(request, id=-1):
    # page 파라미터 추출----------------
    try:
        page = request.GET['page']
    except Exception:
        page = 1
    # ----------------------------------

    # 페이지 정보를 유지
    data = {"id": id, "page": page}

    return render(request, 'board/write.html', data)


# 게시판 일반글 / 답글 등록
def board_write(request, id=-1):
    # page 파라미터 추출----------------
    try:
        page = request.GET['page']
    except Exception:
        page = 1
    # ----------------------------------

    # 게시판 글 공통 정보 추출
    board = Board()
    board.title = request.POST['title']
    board.content = request.POST['content']
    board.user = User.objects.get(id=request.session['authuser']['id'])

    # 게시판 답글 등록
    if id != -1:
        row = Board.objects.get(id=id)
        board.groupno = row.groupno
        board.orderno = row.orderno + 1
        board.depth = row.depth + 1

        # 해당 일반글에 대한 하위 답글의 orderno 칼럼 전부 +1씩 업데이트
        Board.objects.filter(groupno=row.groupno).filter(orderno__gte=board.orderno).update(orderno=F('orderno') + 1)

        board.save()

        return HttpResponseRedirect('/board?page=' + str(page))

    # 게시판 일반글 등록
    max_groupno = Board.objects.aggregate(max_groupno=Max('groupno'))
    board.groupno = 0 if max_groupno['max_groupno'] is None else max_groupno['max_groupno'] + 1

    board.save()

    return HttpResponseRedirect('/board?page=' + str(page))


# 게시판 글 읽기
def board_view(request, id=0):
    # 게시판 글 DB에서 추출
    board = Board.objects.get(id=id)

    # page 파라미터 추출----------------
    try:
        page = request.GET['page']
    except Exception:
        page = 1
    # ----------------------------------

    # 페이지 정보를 유지
    data = {"board": board, "page": page}

    response = render(request, 'board/view.html', data)

    row = Board.objects.get(id=id)

    # 쿠키 로직 - 조회수 업데이트
    # board_list 쿠키가 있을 경우
    if request.COOKIES.get('board_list') is not None:
        board_list = request.COOKIES.get("board_list")

        # 해당 게시글이 전에 본 적이 없을 경우
        if str(id) not in board_list.split(":"):
            board_list += ":" + str(id)
            row.hit += 1

    # board_list 쿠키가 없을 경우
    else:
        board_list = str(id)
        row.hit += 1

    row.save()

    # 쿠키 등록 - 쿠키 만료시간 12시간 설정
    response.set_cookie('board_list', board_list, 3600 * 12)

    return response


# 게시판 삭제
def board_delete(request, id=0):
    row = Board.objects.get(id=id)
    row.remove = 1
    row.save()

    # page 파라미터 추출----------------
    try:
        page = request.GET['page']
    except Exception:
        page = 1
    # ----------------------------------

    return HttpResponseRedirect('/board?page=' + str(page))


# 게시판 수정 양식
def board_modifyform(request, id=0):
    board = Board.objects.get(id=id)

    # page 파라미터 추출----------------
    try:
        page = request.GET['page']
    except Exception:
        page = 1
    # ----------------------------------

    data = {"board": board, "page": page}

    return render(request, 'board/modify.html', data)


# 게시판 수정
def board_modify(request, id=0):
    # 해당 게시판 추출, 수정 후 저장
    row = Board.objects.get(id=id)
    row.title = request.POST['title'] if request.POST['title'] != '' else Board.objects.get(id=id).title
    row.content = request.POST['content']
    row.save()

    # page 파라미터 추출----------------
    try:
        page = request.GET['page']
    except Exception:
        page = 1
    # ----------------------------------

    return HttpResponseRedirect('/board/' + str(id) + "?page=" + str(page))
