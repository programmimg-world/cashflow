from django.urls import path
from . import views

urlpatterns = [
    path('', views.home1, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('terms$condition', views.terms, name='terms'),
    path('privacypolicy', views.privacy, name='privacy'),
    path('aboutus', views.about, name='about'),
    path('login_required', views.login_required, name='login_required'),
    path('generate_otp', views.generate_otp, name='generate_otp'),
    path('send_otp_email', views.send_otp_email, name='send_otp_email'),
]

    #path('logout/', views.logout, name='logout'),

