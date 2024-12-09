# polls/views.py

from django.shortcuts import render,redirect ,get_object_or_404,HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.http import Http404
from .models import Post
from . import models as m
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.http import FileResponse

# Create your views here.
def index(request):
    if request.method == "POST":
        if request.POST.get('action') == '세션삭제1':
            if 'email' in request.session:
                del request.session['email']
                del request.session['name']
            return redirect('main:main')
    author = request.session.get('email')
    if not author:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('main:main')
    post_id = request.GET.get('id')
    if post_id:
        try:
            post = Post.objects.get(pk=post_id) #  데이터베이스에서 해당 조건을 만족하는 객체를 가져오는 ORM 메서드
            print(f"post={post}")                                 #   post_id가 테이블의 기본 키와 일치하는 레코드
            return render(request, 'polls/posting.html', {'post': post})
        except Exception as e:
            messages.error(request, '예기치 못한 오류가 발생했습니다. 다시 시도해주세요.')
    # 모든 Post를 가져와 postlist에 저장
    #postlist = Post.objects.filter(delete=False)
    if request.GET.get('action')=="search":
        try:
            keyword = request.GET.get('search')
            boards = m.search(keyword)
            return render(request, 'polls/index.html', {'boards': boards})
        except Exception as e:
            messages.error(request,f'{e}존재하지 않는 게시글 입니다.')
        return redirect('polls:index')
    else:
        boards = m.list()
        print(boards)
        return render(request, 'polls/index.html', {'boards': boards})

# blog의 게시글(posting)을 부르는 posting 함수
def posting(request):
    post_id = request.GET.get('id')
    user_email = request.session.get('email')
    author = request.session.get('email')

    if not author:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('main:main')
    try:
        m.view(post_id)
        comments= m.comment2(post_id)
        img_url = m.posting(post_id)
        path = img_url[0][0]
        if path is not None:
            filename = path.split('/')[-1]
        else:
            filename = None
        post = get_object_or_404(Post, pk=post_id) # 해당 게시글이 없을경우 에러
    except Exception as e:
        messages.error(request,f'{e}존재하지 않는 게시글 입니다.')
        return redirect('polls:index')
    if post_id and post.del_post==0:
        if request.method =="POST":
            try:
                return HttpResponseRedirect(f'/board/edit?id={post_id}')
            except Exception as e:
                messages.error(request, '예기치 못한 오류가 발생했습니다. 다시 시도해주세요.')
                return redirect('polls:index')
    '''
    if post_id and post.del_post==1: 삭제된 게시판 접근 불가
        messages.error(request, '삭제 처리된 게시글 입니다.')
        return redirect('polls:index')
    '''
    return render(request, 'polls/posting.html', {'post': post ,'user_email': user_email,'filename':filename,'comments':comments}) 

def edit(request):
    post_id = request.GET.get('id')
    author = request.session.get('email')
    if not author:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('main:main')
    if post_id:    
        post = get_object_or_404(Post, pk=post_id)
        if request.method == "POST":
            try:
                post.title = request.POST.get('title')
                post.contents = request.POST.get('contents')
                m.edit(post,post_id) # 데이터베이스에 수정된 내용 저장
                return redirect('polls:index')
            except Exception as e:
                messages.error(request, f'{e}예기치 못한 오류가 발생했습니다. 다시 시도해주세요.')
    return render(request, 'polls/edit.html', {'post': post})

def write(request):
    author = request.session.get('email')
    if not author:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('main:main')
    if request.method == "POST":
        try:
            title = request.POST.get('title')
            contents = request.POST.get('contents')
            name = request.session.get('name')
            email = request.session.get('email')
            try :
                img = request.FILES["imgfile"]
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # MEDIA_ROOT에 저장
                filename = fs.save(img.name, img)
                file_url = f"{request.scheme}://{request.get_host()}{settings.MEDIA_URL}{filename}"
                current_time = datetime.now()
                data = {'title': title, 'name': name, 'contents': contents, 'email': email, 'datetime':current_time.strftime("%Y-%m-%d %H:%M"),'file_url':file_url}
                m.write(**data)
                return redirect('polls:index')
            except KeyError:
                current_time = datetime.now()
                data = {'title': title, 'name': name, 'contents': contents, 'email': email, 'datetime':current_time.strftime("%Y-%m-%d %H:%M")}
                m.write(**data)
                return redirect('polls:index')
        except Exception as e:
            messages.error(request, f'{e}예기치 못한 오류가 발생했습니다. 다시 시도해주세요.')
    return render(request,'polls/write.html')

def delete(request):
    post_id = int(request.GET.get('id'))
    author = request.session.get('email')
    if not author:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('main:main')
    try:
        post = Post.objects.get(pk=post_id)
        if post.email == request.session.get('email'):
            post.del_post = 1
            post.save()
            messages.error(request, '게시글 삭제 처리 되었습니다.')
        else:
            messages.error(request, '작성자가 일치하지 않습니다')
    except Exception as e:
        messages.error(request, '예기치 못한 오류가 발생했습니다. 다시 시도해주세요.')

    return redirect('polls:index')
def download(requset,filename):
    #vs코드 내부용
    file_path = os.path.join("D:/pycharm/mysite/polls/templates/media/"+filename)
    print(file_path)
    response = FileResponse(open(file_path, 'rb'),
                            content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{filename}";path="{file_path}"'
    #아마존
    '''
    def download(requset,filename):
    file_path = os.path.join("/home/ubuntu/mysite/polls/templates/media/"+filename)
    response = FileResponse(open(file_path, 'rb'),
                            content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{filename}"; path="{file_path}"'

    return response
    '''
    
    return response
pass

def comment(request):
    post_id = request.POST.get('id')
    current_time = datetime.now()
    dic = {"post_id":post_id,"comment":request.POST.get("comment"),"name":request.session.get("name"),"email":request.session.get('email'),"creat_at":current_time.strftime("%Y-%m-%d %H:%M")}
    result = m.comment(**dic)
    return redirect(f'/board/view?id={post_id}')
pass

def comment_delete(request):
    post_id = int(request.GET.get('id'))
    author = request.session.get('email')
    if not author:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('main:main')
    try:
        m.comment_del(post_id)
        messages.error(request, '댓글 삭제 처리 되었습니다.')
    except Exception as e:
        messages.error(request, f'{e}예기치 못한 오류가 발생했습니다. 다시 시도해주세요.')

    return redirect('polls:index')