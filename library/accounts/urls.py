from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'accounts'


urlpatterns = [
    path('register/' , register_attempt , name="register_attempt"),
    path('profile-login/' , login_attempt , name="login_attempt"),
    path('token/' , token_send , name="token_send"),
    path('success/' , success , name='success'),
    path('verify/<auth_token>' , verify , name="verify"),
    path('error' , error_page , name="error"),
    path('logout/', logout_view, name='logout'),

    
   
]