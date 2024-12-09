from django.db import models
from django.db import connection

class Post(models.Model):
    title = models.CharField(max_length=50,null=False)
    contents = models.TextField(max_length=254,null=False)
    name = models.CharField(max_length=100,null=False)
    email = models.CharField(max_length=254,null=False)
    created_at = models.DateTimeField(null=True, blank=True)
    views = models.IntegerField(default=0,null=False)
    img_url = models.ImageField(null=True, upload_to="", blank=True)
    del_post = models.BooleanField(default=False,null=False)
    

    class Meta:
        db_table = 'board'  # 데이터베이스 테이블 이름 설정

class Post_Comment(models.Model):
    b_num = models.IntegerField(default=0,null=False)
    comment = models.TextField(max_length=255,null=False)
    name = models.CharField(max_length=100,null=False)
    email = models.CharField(max_length=254,null=False)
    created_at = models.DateTimeField(null=True, blank=True)
    del_comment = models.BooleanField(default=False,null=False)
    class Meta:
        db_table = 'board_comment'

def list():
    query = 'select id,title,name,email,created_at,views from board where del_post=false order by id DESC'
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result
pass

def write(**dic):
    title = dic['title']
    contents = dic['contents']
    name = dic['name']
    email = dic['email']
    date_time = dic['datetime']
    del_post = 0
    try:
        file_url = dic['file_url']
        
        query = f"Insert into board (title,contents,name,email,created_at,img_url,views,del_post) Values('{title}','{contents}','{name}','{email}','{date_time}','{file_url}',0,'{del_post}')"
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except KeyError:
        query = f"Insert into board (title,contents,name,email,created_at,views,del_post) Values('{title}','{contents}','{name}','{email}','{date_time}',0,'{del_post}')"
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    '''
    # ORM을 사용하여 새로운 Post 객체 생성
    new_post = Post(title=title, contents=contents, name=name,email=email)
    new_post.save()  # 데이터베이스에 저장
    '''
pass

def edit(post,id):
    title = post.title
    contents = post.contents
    print(title,contents,id)
    
    '''
    post_to_update = Post.objects.get(pk=id)
    # 업데이트할 내용 설정
    post_to_update.title = post.title
    post_to_update.contents = post.contents
    post_to_update.save()
    return post_to_update
    '''
    
    query = f"update board set contents = '{contents}' where id = '{id}'"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result
pass

def view(post_id):
    query = f"select views from board where id= '{post_id}'"
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        view = cursor.fetchone()
        views = view[0]
        up = f"update board set views = '{views+1}' where id = '{post_id}'"
        result = cursor.execute(up)
    return result
pass


def search(keyword):
    query = f"select id,title,name,email,created_at,views from board where del_post=false and title LIKE '%{keyword}%' order by id DESC"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result
pass

def posting(post_id):
    query = f"select img_url from board where id ='{post_id}'"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result
pass

def comment(**dic):
    b_num = dic['post_id']
    comment = dic['comment']
    name = dic['name']
    email = dic['email']
    creat_at = dic['creat_at']
    sql = f"Insert into board_comment(b_num,comment,name,email,created_at,del_comment) Values('{b_num}','{comment}','{name}','{email}','{creat_at}',0)"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    return result

pass


def comment2(post_id):
    sql = f"select id,comment,name,email,created_at from board_comment where b_num = '{post_id}' and del_comment=False order by id DESC"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    return result

pass

def comment_del(post_id):
    sql = f"update board_comment set del_comment = True where id = '{post_id}'"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    return result