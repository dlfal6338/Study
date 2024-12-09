from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser
from django.contrib import messages
from . import models
from django.contrib.auth.hashers import check_password,make_password

def home(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'accounts/home.html', context)
pass

def register(request):
    if request.method == "POST":
        email = request.POST['email']
        name = request.POST['name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if email.strip() and name.strip() and password1.strip() and password2.strip():
            if password1 == password2: 
            # CustomUser 인스턴스 생성
                try:
                    CustomUser.objects.create_user(
                        username=email,
                        email=email,  
                        name=name,  
                        password=password1
                    )
                    return redirect('main:main')
                except Exception as e:
                    print(f"예외 발생: {e}")
                    if(e.args[0]==1062):
                        messages.error(request, '이메일 중복.')
                        return redirect('accounts:register')
                    else:
                        messages.error(request, '예기치 못한 오류가 발생했습니다. 다시 시도해주세요.')
                        return redirect('accounts:register')
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
                return redirect('accounts:register')
        else:
            messages.error(request, '빈칸을 확인해주세요.')
            return redirect('accounts:register')
    return render(request, 'accounts/register.html')
pass

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        login_data = {
            'email': email,
            'password': password
        }
        user_data = models.Login_Check(**login_data)
        if user_data is not None:
            try:
                print("로그인 성공")
                request.session['email'] = user_data[0]
                request.session['name'] = user_data[2]
                print(user_data[2])
                return redirect('polls:index')
            except Exception as e:
                print(f"예외 발생: {e}")
                messages.error(request, f'예기치 못한 오류가 발생했습니다. 다시 시도해주세요.\n{e}')
                return redirect('accounts:login')
        else:
            print("로그인 실패")
            messages.error(request, '아이디 또는 비밀번호가 일치하지 않습니다.')
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')
pass

def login2(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        login_data = {
            'email': email,
            'password': password
        }
        user_data = models.Login_Check2(**login_data)
        print(user_data)
        if user_data[0][1] == password:
            try:
                print("로그인 성공")
                request.session['email'] = user_data[0][0]
                request.session['name'] = user_data[0][2]
                return redirect('polls:index')
            except Exception as e:
                print(f"예외 발생: {e}")
                messages.error(request, f'예기치 못한 오류가 발생했습니다. 다시 시도해주세요.\n{e}')
                return redirect('accounts:login2')
        else:
            print("로그인 실패")
            messages.error(request, '아이디 또는 비밀번호가 일치하지 않습니다.')
            return redirect('accounts:login2')
    
    return render(request, 'accounts/login2.html')
pass