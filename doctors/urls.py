# healthcare/urls.py
from django.urls import path
from doctors.views import (
    # Doctor Views
    doctor_dashboard, doctor_patient,doctor_profile,
    weekly_schedule, take_leave, doctor_calendar, calendar_events_api,
    doctor_slots, doctor_appointment_detail, mark_appointment_complete,
    donging, dupcoming, doutgoing,
    showAppointment, docprescription, get_appointment_info,
)

urlpatterns = [
    # ====================== DOCTOR PORTAL ======================
    path('', doctor_dashboard, name='doctor_dashboard'),
    path('patients',doctor_patient,name="doctor_patients"),
    path('profile/', doctor_profile, name='doctor_profile'),
    path('weekly-schedule/', weekly_schedule, name='weekly_schedule'),
    path('take-leave/', take_leave, name='take_leave'),
    path('calendar/', doctor_calendar, name='doctor_calendar'),
    path('api/calendar-events/', calendar_events_api, name='calendar_events_api'),
    path('slots/', doctor_slots, name='doctor_slots'),

    # Appointments
    path('appointments/ongoing/', donging, name='dongoing'),
    path('appointments/upcoming/', dupcoming, name='dupcoming'),
    path('appointments/past/', doutgoing, name='doutgoing'),
    # In healthcare/urls.py (doctor section)
    path('doctor/appointment/<int:appt_id>/', doctor_appointment_detail, name='doctor_appointment_detail'),
    path('doctor/appointment/<int:appt_id>/complete/', mark_appointment_complete, name='mark_complete'),  # optional

    # Prescription
    path('send-prescription/', showAppointment, name='showAppointment'),
    path('prescriptions/', docprescription, name='docprescription'),
    path('ajax/get-appointment-info/', get_appointment_info, name='get_appointment_info'),
]