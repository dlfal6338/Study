# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models,connection
from .managers import CustomUserManager
import pymysql

class CustomUser(AbstractUser):  #
    name = models.CharField(max_length=100) 
    email = models.EmailField(unique=True)
    # password = models.CharField(max_length=100) # 기본 제공


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()  # 커스텀 매니저 설정

    class Meta:
        db_table = 'users'  # 데이터베이스 테이블 이름 설정

def Login_Check(**dic):

    email = dic['email']
    password = dic['password']

    query = "SELECT email,password,name FROM users WHERE email = '" + email + "' AND password = '" + password + "'"

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    #cursor는 with 블록이 끝날 때 자동으로 닫힘
    #Django에서는 일반적으로 데이터베이스 연결은 프레임워크가 관리하므로 수동으로 닫을 필요가 없음

    return result
pass

def Login_Check2(**dic):
    email = dic['email']
    query = f"SELECT email,password,name FROM users WHERE email = '{email}'"
    with connection.cursor() as cursor:
        cursor.execute(query)
        #result = cursor.fetchone()
        #for email,password,name in cursor:
        #    result = (email,password,name)
        result = cursor.fetchall()
    return result

pass