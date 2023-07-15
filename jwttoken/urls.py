"""jwttoken URL Configuration

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
from rest_framework_simplejwt.views import  TokenRefreshView



from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import admin
from django.urls import path
from appi import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', views.UserApi.as_view(), name='user'),
    path('studentapi/', views.StudentApi.as_view(), name='stu'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileViewApi().as_view(), name='profile'),
    path('changepass/', views.ChangePassApi.as_view(), name='changepass'),
]
