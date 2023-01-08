import imp
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
import requests 
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Categories , Course , Level , Video , Usercourse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages



def home(request):
    category = Categories.objects.all().order_by('id')[0:6 ]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    x = {
        'category':category,
        'course':course
    }
    return render(request , 'Main/home.html' , x)




def pagecourse(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    freecourse = Course.objects.filter(price = 0).count()
    pricecourse = Course.objects.filter(price__gte=1).count()
    
    x={
        'category':category,
        'level':level,
        'course':course,
        'freecourse':freecourse,
        'pricecourse':pricecourse
    }
    return render(request , 'Main/pagecourse.html' , x)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print(price)


    if price == ['pricefree']:
       course = Course.objects.filter(price=0)
    elif price == ['pricepaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
       course = Course.objects.all()
    elif categories:
       course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
       course = Course.objects.all().order_by('-id')


    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})


def about_uspage(request):
    category = Categories.get_all_category(Categories)
    x={
        'category':category,
    }
    return render(request , 'Main/about_uspage.html' , x)

def contact_uspage(request):
    category = Categories.get_all_category(Categories)
    x={
        'category':category,
    }
    return render(request , 'Main/contact_uspage.html' , x)

def SEARCH_COURSE(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    context = {
        'course':course,
    }
    return render(request,'search/search.html',context)

def page_notefound(request):
    category = Categories.get_all_category(Categories)
    x={
        'category':category,
    }
    return render(request,'error/404.html' , x)

def course_details(request , slug):
    category = Categories.get_all_category(Categories)
    time= Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_der'))
    
    course_id = Course.objects.get(slug =slug)
    try:
        check_enrool = Usercourse.objects.get(user = request.user, course = course_id )
    except Usercourse.DoesNotExist:
        check_enrool = None
        
    course = Course.objects.filter(slug = slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('app:404')
    x={
        'course':course, 
        'category':category,
        'time':time,
        'check_enrool':check_enrool,
    }
    return render(request,'course/course_details.html' , x)

def chackout(request , slug):
    course = Course.objects.get(slug=slug)
    if course.price == 0:
        course= Usercourse(
            user = request.user,
            course = course,
            
        )
        course.save()
        messages.success(request,'!تم التسجيل في الدورة')
        return redirect('app:mycourse')
        
    return render(request , 'chackout/chackout.html' , )


def mycourse(request):
    course = Usercourse.objects.filter(user = request.user)
    return render(request , 'course/mycourse.html' , {'course':course})


def watchcourse(request , slug):
    lectucr = request.GET.get('lectucr')
    course_id= Course.objects.get(slug =slug)
    course = Course.objects.filter(slug =slug)
    try:
        video = Video.objects.get(id =lectucr )
        if course.exists():
            course =course.first()
        else:
            return redirect("app:404")
               
    except Usercourse.DoesNotExist:
        return redirect("app:404")
    
    x={
       'course':course ,
       'video':video,
       'lectucr':lectucr
    }
    return render(request , 'course/watchcourse.html' , x)