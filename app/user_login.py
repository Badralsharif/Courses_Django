from django.shortcuts import redirect, render
from django.contrib.auth.models import User 
from django.contrib import messages
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login,logout 
from app.models import*
def REGISTER(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # check email
        if User.objects.filter(email=email).exists():
           messages.warning(request,'!البريد الالكتروني موجود')
           return redirect('app:register')
        # check username
        if User.objects.filter(username=username).exists():
           messages.warning(request,' ! الاسم موجود')
           return redirect('app:register')
        user = User(
            username=username,
            email=email, )
        user.set_password(password)
        user.save()
        return redirect('app:login')
    return render (request , 'registration/register.html' , {})


	
def DOLOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
		
        user = EmailBackEnd.authenticate(request,
                                     username=email,
                                     password=password)
        if user!=None:
           login(request,user)
           return redirect('app:home')
        else:
           messages.error(request,'Email and Password Are Invalid !')
           return redirect('app:login')
		   
def Profile(request): 
    category = Categories.get_all_category(Categories)
    x={
        'category':category,
    }
    return render (request , 'registration/profile.html' , x)
def password_reset_confirm(request): 
    return render (request , 'registration/password_reset_confirm.html' , {})
    

def  PROFILE_UPDATE(request): 
     if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'تم التحديث بنجاح. ')
        return redirect('app:login')
    