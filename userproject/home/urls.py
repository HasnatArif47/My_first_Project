from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index,name='home'),
    path('login/',views.loginuser,name='login'),
    path('logout/',views.logoutuser,name='logout'),
    path('signup/', views.signupuser, name='signup'), 
    path('adminpanel/', views.admin, name='admin'),
    path('adminpanel/signup/', views.signupuser, name='admin'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('save_user_info/', views.save_user_info, name='save_user_info'),
    path('success/', views.success, name='success'), 
    path('save_user_info/', views.save_user_info, name='save_user_info'),  
    ]
