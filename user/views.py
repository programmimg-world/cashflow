from django.shortcuts import render, redirect
from django.contrib.sessions.backends.db import SessionStore
from .models import *
import random
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
# for security

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        email = request.session.get('email')
        if email:
            print('Email from session:', email)
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper

# Generate OTP
def generate_otp():
    otp = random.randint(100000, 999999)
    return str(otp)

# Send OTP via email
def send_otp_email(request):
    email = request.POST.get('email')
    if email:
        otp = generate_otp()
        request.session['otp'] = otp  # Save OTP in session
        message = f"Your OTP: {otp}"
        send_mail('OTP Verification', message, settings.DEFAULT_FROM_EMAIL, [email])
        return render(request, 'register.html', {'enter_otp': True})
    else:
        error_message = 'Invalid email. Please try again.'
        return render(request, 'register.html', {'error_message': error_message})


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        enterotp = request.POST.get('eotp')
        stored_otp = request.session.get('otp')
        if not (email and name and password and confirmpassword):
            # Required fields are not filled
            error_message = 'Please fill in all the required fields.'
            return render(request, 'register.html', {'error_message': error_message})
        elif not stored_otp:
            # No OTP in session
            error_message = 'OTP verification is required.'
            return render(request, 'register.html', {'error_message': error_message})
        elif enterotp == stored_otp:
            # OTP is valid
            if Userdata.objects.filter(email=email).exists():
                error_message = "User Already Exists"
                return render(request, 'register.html', {'error_message': error_message})

            elif password == confirmpassword:
                data = Userdata(email=email, name=name, password=confirmpassword)
                data.save()
                # Clear the OTP from session
                del request.session['otp']
                return redirect('login')
            else:
                error_message = "Passwords Don't Match"
                return render(request, 'register.html', {'error_message': error_message})
        else:
            # Invalid OTP
            error_message = 'Invalid OTP. Please try again.'
            # Clear the OTP from session
            del request.session['otp']
            return render(request, 'register.html', {'error_message': error_message})
    else:
        # GET request, render the registration form
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('gmail')
        password = request.POST.get('pass')
        checkbox = request.POST.get('robot-checkbox')

        if checkbox == 'checked':  # Check if the checkbox value is 'checked' when checked
            # Checkbox is checked
            if Userdata.objects.filter(email=email, password=password).exists():
                session = SessionStore()
                session['email'] = email
                session.create()
                # Store the session key in the cookie
                response = redirect('main')
                response.set_cookie('sessionid', session.session_key)
                # Print debug message to check if session is created and email value is stored
                print('Session created:', session.session_key)
                print('Email stored in session:', session['email'])
            

                return response
            else:
                error_message = 'Invalid Credentials'
                return render(request, 'login.html', {'error_message': error_message})
        else:
            # Checkbox is not checked
            error_message = "Please verify that you're not a robot."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')
    

def home1(request):
    return render(request, 'home.html')

def terms(request):
    return render(request, 'terms$condition.html')

def privacy(request):
    return render(request, 'privacypolicy.html')

def about(request):
    return render(request, 'aboutus.html')


