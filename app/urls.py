from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import user_login, views


app_name = 'app'
urlpatterns = [
    path('' , views.home , name='home'),
    path('404' , views.page_notefound , name='404'),
    path('pagecourse' , views.pagecourse , name='pagecourse'),
    path('course/filter-data',views.filter_data,name="filter-data"),
    path('course/<slug:slug>',views.course_details,name="course_details"),
    path('search',views.SEARCH_COURSE,name='search_course'),
    path('about_uspage' , views.about_uspage , name='about_uspage'),
    path('contact_uspage' , views.contact_uspage , name='contact_uspage'),
    path('accounts/register', user_login.REGISTER , name = 'register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin/', user_login.DOLOGIN, name = 'doLogin'),
    path('accounts/profile' , user_login.Profile , name='profile'),
    path('accounts/profile/update', user_login.PROFILE_UPDATE , name='profile_update'),
    path('accounts/password_reset_confirm', user_login.password_reset_confirm , name='password_reset_confirm'),
    
    path('chackout/<slug:slug>',views.chackout,name="chackout"),
    path('mycourse',views.mycourse,name="mycourse"),
    path('course/watchcourse/<slug:slug>',views.watchcourse,name="watchcourse"),

] + static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)
  