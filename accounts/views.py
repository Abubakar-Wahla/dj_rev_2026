from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def login_user(request):

    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user =authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'Logged in successfully')

            next_url=request.GET.get('next')

            if next_url:
                return redirect(next_url) 
            
            else:
                return redirect('home')
        
        else:
            messages.error(request,'Invalid username or password')

    return render(request,'accounts/login.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request,"accounts/dashboard.html")

def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')

        if password1 != password2:
            messages.error(request,'Passwords do not match')
            return render("accounts/register.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already taken')
            return render("accounts/register.html")
        
        user=User.objects.create_user(username=username,email=email,password=password1)
        messages.success(request,'Account created successfully')

        login(request,user)
        return redirect('dashboard')
    
    return render(request,"accounts/register.html")
