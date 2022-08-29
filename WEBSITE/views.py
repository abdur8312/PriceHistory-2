from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from WEBSITE.models import Register
from django.db import connection

def temp(request):
    return render(request, 'temp.html')

def index(request):
    #return render(request, 'index.html')
    return HttpResponse('returned')

def login(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        password = request.POST['password']

        #The below statement is used to compare username and password with the database using RAW QUERIES
        cursor = connection.cursor()
        cursor.execute(''' SELECT user_name,password FROM register WHERE user_name=%s AND password=%s ''', [user_name, password])
        row = cursor.fetchone()

        request.session.set_expiry(86400)  #used to add sessions in the database table
        if row is not None:
            return redirect('product')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')

def register(request):

    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['user_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if Register.objects.filter(user_name=user_name).exists():
                messages.info(request, 'Username already taken')
                return redirect('register')
            elif Register.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('register')
            else:
                user = Register.objects.get_or_create(email=email,
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                    user_name=user_name,
                                                    password=password1)
                print("user created")
                return redirect('index')
        else:
            messages.info(request, 'password not matching!!!')
            return redirect('register')
        return redirect('index')
    else:
        return render(request, 'register.html')

def product(request):
    return render(request, 'product.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
