"""luffyuecheng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import re_path, include
# from django.shortcuts import resolve_url
from django.shortcuts import HttpResponse
from django.contrib.admin import site


# from django.contrib.staticfiles.views import serve

def test(request):
    print(type(request))
    return HttpResponse('Welcome to LuffyCity')


urlpatterns = [
    re_path('admin/', site.urls),
    re_path('test/', test, name='test'),
    re_path('api/(?P<version>\w+)/', include(('luffyapi.urls', 'luffyapi'), namespace='luffyapi'))
]
