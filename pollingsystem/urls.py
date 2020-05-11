"""pollingsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, re_path
# from django.contrib.auth import login, logout
from pollingsystem.views import index

urlpatterns = [
    re_path(r'^poll/', include('poll.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', index, name='index'),
    re_path(r'', include('django.contrib.auth.urls'))
]
