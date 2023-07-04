"""toddle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from .views import *
from home import views

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('',LoginView.as_view()),
    path('ShowFeed/<id>',views.ShowFeed.delete),
    path('update',views.ShowFeed.put),
    path('logout',LogoutView.as_view()),
    path('ShowFeed',ShowFeed.as_view()),
    path('Upload',UploadFeed.as_view()),
    
    # path('doc',DocumentView.as_view()),
    
    # path('S_register',S_RegisterView.as_view()),
    # path('S_login',S_LoginView.as_view()),
    # path('S_user',S_UserView.as_view()),
    # path('S_logout',S_LogoutView.as_view()),

]
