from django.db.models import F
from django.shortcuts import render, redirect

# Create your views here.
# 게시판 목록보기 처리
from django.views.decorators.cache import cache_control

from board.models import Board
from member.models import Member


# 데코레이터로 웹페이지의 캐시기능를 중지함
@cache_control(no_cashe=True, no_store=True, must_revalidate=True)
# 바로 아래있는 함수 하나에만 적용
def list(request):
    # select 'id', 'title', 'userid', 'regdate', 'views'
    # from board order by id desc
    # bdlist = board.objects.values(
    #     'id', 'title', 'userid', 'regdate', 'views')\
    #     .order_by('-id')

    # board와 Member 테이블은 userid <-> id 컬럼을 기준으로
    # inner join

    bdlist = Board.objects.select_related('member')

    # join된 member 테이블의 userid 확인
    # bdlist.get(0).member.userid
    context = {'bds': bdlist}

    return render(request, 'board/list.html', context)


#게시판 본문보기 처리

def view(request):
    if request.method == 'GET':
        form = request.GET.dict()
        # print(form['bno'])
        # 본문글에 대한 조회수 증가
        # update.board set view = views + 1
        # where id = ???
        # b = Board.objects.get(id=form['bno'])
        # b.views = b.views + 1
        # b.save()
        Board.objects.filter(id=form['bno']).update(views=F('views') + 1)

        # 본문글 조회
        # select * from board inner join member
        # where(id) where id = ???
        bd = Board.objects.select_related('member').get(id=form['bno'])

    elif request.method == 'POST':
         pass

    context = {'bd': bd}
    return render(request, 'board/view.html', context)


# 게시판 글쓰기 처리
# get : board/write.html
# post : 작성한 글을 디비에 저장, board/lisr.html로 이동
def write(request):
    returnPage = 'board/write.html'
    form = ''
    error = ''

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        form = request.POST.dict()

        # 유효성 검사1
        if not(form['title'] and form['contents']):
            error = '제목이나 본문을 작성하세요!'

        else:
            # 입력한 게시글을 Board객체에 담음
            bd = Board(title=form['title'],
                       contents=form['contents'],
                       # 새 글을 작성한 회원에 대한 정보는
                       # 회원테이블에 존재하는 회원아이디(id)를 조회해서
                       # userid속성에 저장
                       member=Member.objects.get(pk=form['memberid']))  # 테이블에 저장
            bd.save() #Board객체에 담은 게시글을 테이블에 저장
            return redirect('/list')

    context = {'form': form, 'error': error}
    return render(request, returnPage, context)

# 본문글 삭제하기
# /remove?
def remove(request):
    if request.method == 'GET':
        form = request.GET.dict()

        # delete from board where bno = ??
        Board.objects.filter(id=form['bno']).delete();

    return redirect('/list')

# 본문글 수정하기
def modify(request):
    if request.method == 'GET':
        form = request.GET.dict()

        # select * from board where bno = ???
        bd = Board.objects.get(id=form['bno'])
    elif request.method == 'POST':
            form = request.POST.dict()

            # update board set title = ???, contents = ???
            # where bno = ???

            # b = Board.objects.get(id=form['bno'])
            # b.title = form['title']
            # b.contents = form['contents']
            # b.save()

            Board.objects.filter(id=form['bno']).update(title=form['title'], contents=form['contents'])
            # 본문글 수정완료시
            return redirect('/view?bno=' + form['bno'])

    context = {'bd': bd}
    return render(request, 'board/modify.html', context)

