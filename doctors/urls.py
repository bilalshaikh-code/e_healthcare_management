from django.urls import path
from . import old_views
from .views import auth
from django.contrib.auth import views as auth_views

urlpatterns=[
   #  my urls here.
   path('dashboard', old_views.dashboard, name='doctor_dashboard'),
   path('dashboard/appointment',old_views.my_appointment,name="doctor_appoinment"),
   path('dashboard/patients',old_views.my_patients,name="doctor_patients"),
   path('profile',old_views.my_profile,name="doctor_profile"),

   # Auth urls here.
   path('register',auth.register, name='doctor_register'),
   
   

   path('logout',old_views.logout,name='logout'),
   path('dabout1', old_views.dabout1, name='dabout1'),
    
   path('dservice', old_views.dservice, name='dservice'),
   path('dcontact1', old_views.dcontact1, name='dcontact1'),
   path('showAppointment', old_views.showAppointment, name='showAppointment'),
   path('drSchedule', old_views.drSchedule, name='drSchedule'),
   path('dongoing',old_views.dongoing,name='dongoing'),
   path('dupcoming',old_views.dupcoming,name='dupcoming'),
   path('dupcoming1',old_views.dupcoming1,name='dupcoming1'),
   path('doutgoing',old_views.doutgoing,name='doutgoing'),
   path('docprescription',old_views.docprescription,name='docprescription'),
   path('get_appointment_info',old_views.get_appointment_info, name='get_appointment_info'),
 
]