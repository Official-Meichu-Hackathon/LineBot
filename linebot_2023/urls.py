"""
URL configuration for linebot_2023 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from mainbot import views #MylinebotApp改成自己藍色的資料夾

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mainbot/', include('mainbot.urls')), #包含應用程式的網址
    path('callback',views.callback),
    path('callback/',views.callback)
]