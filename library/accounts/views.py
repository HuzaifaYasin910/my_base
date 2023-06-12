from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
EMAIL_ADDRESS  = 'novelsnotions@gmail.com'
EMAIL_PASSWORD = 'tsojwmidjtrgnavv'
from django.conf import settings

from django.contrib.auth import logout

from django.core.mail import send_mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

# Create your views here.





def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/profile-login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('//profile-login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('//profile-login')
        
        login(request , user)
        return redirect('/profile-login')

    return render(request , 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('/home') 


def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is already taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is already taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            
            send_email(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)


    return render(request , 'accounts/register.html')

def success(request):
    return render(request , 'accounts/success.html')


def token_send(request):
    token_sent= True
    return render(request , 'accounts/token_send.html',{'token_sent':token_sent})



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'accounts/error.html')




def send_email(email,token):
    
    subject = 'Your account needs to be verified'
    message = f"Hi please click the link to verify your account http://127.0.0.1:8000/verify/{token} \n please ignore this email if this weren't you "
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()




    