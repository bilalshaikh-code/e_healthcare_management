# healthcare/urls.py
from django.urls import path
from healthcare.views import (
    # Auth
    register, login_view, logout_view,
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView,
    # Patient Views
    patient_dashboard, patient_profile,
    book_appointment, get_available_slots, confirm_booking,
    my_appointments, cancel_appointment, my_prescriptions,
    prescription_detail, download_prescription_pdf, appointment_history,
)
from healthcare.views import index

urlpatterns = [
    # 
    path('',index.home,name='index'),
    path('home',index.home,name='home'),
    path('about',index.about,name="about"),
    path('service',index.service,name="service"),
    path('feedback',index.feedback,name="feedback"),
    path('contact',index.contact,name='contact'),

    # ====================== AUTH ======================
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Password Reset Flow
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # ====================== PATIENT PORTAL ======================
    path('patient/dashboard/', patient_dashboard, name='patient_dashboard'),
    path('patient/profile/', patient_profile, name='patient_profile'),
    
    # Booking
    path('patient/book/', book_appointment, name='book_appointment'),
    path('patient/api/slots/', get_available_slots, name='get_available_slots'),
    path('patient/confirm-booking/', confirm_booking, name='confirm_booking'),
    
    # Appointments
    path('patient/appointments/', my_appointments, name='my_appointments'),
    path('patient/appointment/<int:appt_id>/cancel/', cancel_appointment, name='cancel_appointment'),
    path('patient/appointment/<int:pk>/', prescription_detail, name='appointment_detail'),  # optional detail page
    path('patient/history/', appointment_history, name='appointment_history'),

    # Prescription
    path('patient/prescriptions/', my_prescriptions, name='my_prescriptions'),
    path('patient/prescription/<int:pk>/', prescription_detail, name='prescription_detail'),
    path('patient/prescription/<int:pk>/pdf/', download_prescription_pdf, name='download_prescription_pdf'),
]