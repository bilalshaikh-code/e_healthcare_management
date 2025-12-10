from django.urls import path
from . import views_old as views
from .views import pages, auth, profile, patient
from django.contrib.auth import views as auth_views

urlpatterns=[
    # these urls are pages links
    path('',pages.index,name='index'),
    path('home',pages.index,name='home'),
    path('home/about',pages.about,name='about'),
    path('home/contact',pages.contact,name='contact'),
    path('home/service',pages.services,name='service'),
    path('home/service/<int:service_id>/', pages.service_detail, name='service_detail'),
    path('home/pricing',pages.pricing,name='price'),
    path('home/complain',pages.complain,name='complain'),
    path('home/feedback',pages.feedback,name='feedback'),

    # Authentication urls here.
    path('register',auth.register,name='register'),
    path('login',auth.signin,name='signin'),
    path('logout',auth.logout,name='logout'),
    path('reset_password',auth_views.PasswordResetView.as_view(template_name="auth/reset_password.html"),name="password_reset"),
    path('password_reset_done',auth_views.PasswordResetDoneView.as_view(template_name="auth/reset_password_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"),name="password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name="auth/reset_password_complete.html"),name="password_reset_complete"),
    
    # profile urls here.
    path('home/profile',profile.view,name='p_view'),
    path('home/profile/update',profile.update,name='update_user'),

    # patient related urls here.
    path('home/patient/outgoing',patient.outgoing,name='outgoing'),
    path('home/patient/ongoing',patient.ongoing,name='ongoing'),
    path('home/patient/upcoming',patient.upcoming,name='upcoming'),
    path('home/patient/prescription',patient.prescription,name='prescription'),

    # appointment related urls here.
    path('home/appointment',pages.appointment,name='appointment'),




    path('paymentinvoice.html',views.paymentinvoice,name='paymentinvoice'),
    path('get_doctors/', views.get_doctors, name='get_doctors'),
    path('get_slots/', views.get_slots, name='get_slots'),
    
    path('success',views.OrderSuccess,name='success'),
    path('updateAppointment',views.updateAppointment,name='updateAppointment'),
]