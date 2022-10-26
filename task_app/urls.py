from django.urls import path
from .views import register, login_user, home, check_url

urlpatterns = [
    path('register/', register, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('', home, name='home'),
    path('check_url/', check_url, name='check_url'),

]
