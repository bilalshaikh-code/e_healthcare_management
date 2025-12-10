from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
# Create your views here.
# from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
# from .forms import DoctorLoginForm
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError

# def doctor_login(request):
#     if request.method == 'POST':
#         form = DoctorLoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             doctor = authenticate(request, email=email, password=password)
#             if doctor is not None:
#                 login(request, doctor)
#                 return redirect('/')  # Redirect to doctor dashboard after login
#             else:
#                 # Handle invalid login
#                 pass
#     else:
#         form = DoctorLoginForm()
#     return render(request, 'doctor_login.html', {'form': form})

# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from .forms import  UserLoginForm
from healthcare.models import *

def email_exists(email):
    return Doctor.objects.filter(email=email).exists()

def dashboard(request):
    dests=Destination.objects.all()
    feedback=Feedback.objects.all()
    AddDr=Doctor.objects.all()

    return render(request,'doctor/dashboard.html',{'dests':dests,'feedback':feedback,'AddDr':AddDr})

# def doctor_login(request):
#     try:
#         if request.method=='POST':
#             email=request.POST['email']
#             password=request.POST['password']
#             user = auth.authenticate(email=email,password=password)
#             if user is not None:
#                 if email_exists(email):
#                     auth.login(request,user)
#                     return redirect("/")
#                 else:
#                     messages.info(request,"invalid credentials")
#                     return redirect("signin")
#             else:
#                 messages.info(request,"invalid credentials")
#                 return redirect("signin")
#         else: 
#             return render(request,'signin.html')
        
#     except MultiValueDictKeyError as e:
#         print(f"Error: {e}")
#         print(f"request.POST: {request.POST}")
#         return HttpResponse('Error occurred') 
    
def logout(request):
    auth.logout(request)
    return redirect('/')


def dabout1(request):
    AddDr=Doctor.objects.all()
    return render(request,'dabout1.html',{'AddDr':AddDr})

def dservice(request):
    feedback=Feedback.objects.all()
    return render(request,'dservice.html',{'feedback':feedback})

from django.core.mail import send_mail
def dcontact1(request,):  
    if request.method=='POST':
        name=request.POST['name']
        subject=request.POST['subject']
        email=request.POST['email']
        msg=request.POST['message']
        contact = ContactUs.objects.create(
            name=name,
            email=email,
            subject=subject,
            msg=msg)
        send_mail(
            subject,#subject
            msg,#message
            contact.email,#from email
            ['tirth5524@gmail.com']# to email
        )
        return render(request,'contact1.html',{'name':name})
    else :
        return render(request,'dcontact1.html',{})
# def Appointment_exists(Appointment_ID):
    
#     return Appointment.objects.filter(id=Appointment_ID).exists()
def showAppointment(request):

    if request.user.is_authenticated:
        if request.method=='POST':
            # form_data = request.POST
            # print(form_data)
            date=request.POST['date']
            Appointment_ID=request.POST['Appointment_ID']
            patientName=request.POST['patientName']
            prescription=request.POST['prescription']
            chat=request.POST['chat']
            # h=Appointment.objects.get(id=Appointment_ID)
            # print(h.patientid.email)
            # print(form_data)

            try:
                if Appointment.objects.filter(id=Appointment_ID).exists():
                # if Appointment_exists(Appointment_ID):
                        # print("hi")
                        h=Appointment.objects.get(id=Appointment_ID)
                        email1=h.patientid.email
                        sw = ShowAppointment.objects.create(
                            appointment_id=h,
                            date=date,
                            prescription=prescription,
                            chat =chat
                        )
                        print(sw)
                        send_mail(
                        "Prescription From HealthPlus Doctor",#subject
                        "Appointment_ID :"+Appointment_ID+"\n"+"Date :"+patientName+"\n"+"Precscription : "+prescription+" \n"+"Chat :"+chat,#message
                        'prajapatitirth031@gmail.com',#from email
                        ['tirth5524@gmail.com',email1]# to email
                        )
                        # HttpResponse("Success :")
                        messages.info(request,"You Have Successfuly sent Prescription :")
                        print("h2")
                        # return redirect("showAppointment")
                        return redirect('doctor')
                else: 
                    print("hi3")
                    messages.info(request,"Somthing Went Wrong Please Check Appointment Id ....!:")
                    # return redirect("showAppointment")
                    return render(request,'showAppointment.html')
            except:
                
                messages.info(request,"Somthing Went Wrong Please Check Appointment Id ....!:")
                # return redirect("doctors/showAppointment")
                return render(request,'showAppointment.html')
            
        # app=Appointment.objects.all()
        return render(request,'showAppointment.html')
    else :
        return render(request,'showAppointment.html')
  
def drSchedule(request):
    # try:
        slots=Slot.objects.all()
        if request.user.is_authenticated:
           
            if request.method=='POST':
                # form_data = request.POST
                # print(form_data)
                date=request.POST['date']
                slottime=request.POST['time']
                # status=request.POST['status']
                slotID = Slot.objects.get(id=slottime)
                puser= CustomUser.objects.get(id=request.user.id)
                id1 = Doctor.objects.get(email=puser.email)
                sw = DoctorSchedule.objects.create(
                            doctorid=id1,
                            slotid=slotID,
                            date=date,
                            status =True
                        )
                print(sw)
                messages.success(request, "Slot Added Successfully.")
                return render(request,'drSchedule.html',{'slots':slots})
                

        return render(request,'drSchedule.html',{'slots':slots})
    # except:

def dongoing(request):
    if request.user.is_authenticated:
        puser= CustomUser.objects.get(id=request.user.id)

        id1 = Doctor.objects.get(email=puser.email)
        # print(id1)
        current1 = Appointment.objects.filter(doctorid=id1.id)
        # print(puser)
        current=[]
        t2=datetime.today().date()
        past=[]
        for i in current1:
            if t2<= i.date:
                current.append(i)
            else:
                past.append(i)

        # print(past)
        # for i in current:
        #     # slot= Slot.objects.filter(id=i.slotid)
        #     # i.slotid=slot.slot_time
        #     print(f"{i.id}, {i.patientid}, {i.doctorid.id},{i.date}, {i.slotid.slot_time}")
        if request.method=='POST':
            # print("hi")
            form_data = request.POST
            if 'actioncnl' in form_data:
                cancel_value = request.POST['actioncnl']
                # print(cancel_value,'h')
                Appointment.objects.filter(id=cancel_value).delete()
                # return HttpResponse("Success Deleted")
                return redirect("dongoing")
    
        else:
            return render(request,'dongoing.html',{"current":current})
    else:
       return HttpResponse("you are not authenticated to see this page :")
    
def doutgoing(request,):
    if request.user.is_authenticated:
        puser= CustomUser.objects.get(id=request.user.id)
        id1 = Doctor.objects.get(email=puser.email)
        # print(id1)
        current1 = Appointment.objects.filter(doctorid=id1.id)
        t2=datetime.today().date()
        past=[]
        for i in current1:
            if t2>i.date:
                
                past.append(i)      
        return render(request,'doutgoing.html',{"past":past})
    else:
       return HttpResponse("you are not authenticated to see this page :")
    
def dupcoming(request):

    if request.user.is_authenticated:
        puser= CustomUser.objects.get(id=request.user.id)

        id1 = Doctor.objects.get(email=puser.email)
        # print(id1)
        current1 = Appointment.objects.filter(doctorid=id1.id)
        # print(puser)
        current=[]
        t2=datetime.today().date()
        past=[]
        for i in current1:
            if t2< i.date:
                current.append(i)
            else:
                past.append(i)

        # print(past)
        # for i in current:
        #     # slot= Slot.objects.filter(id=i.slotid)
        #     # i.slotid=slot.slot_time
        #     print(f"{i.id}, {i.patientid}, {i.doctorid.id},{i.date}, {i.slotid.slot_time}")
        if request.method=='POST':
            # print("hi")
            form_data = request.POST
            if 'actioncnl' in form_data:
                cancel_value = request.POST['actioncnl']
                # print(cancel_value,'h')
                Appointment.objects.filter(id=cancel_value).delete()
                # return HttpResponse("Success Deleted")
                return redirect("dupcoming")
    
        else:
            return render(request,'dupcoming.html',{"current":current})
    else:
       return HttpResponse("you are not authenticated to see this page :")
    
def dupcoming1(request):

    if request.user.is_authenticated:
        puser= CustomUser.objects.get(id=request.user.id)

        id1 = Doctor.objects.get(email=puser.email)
        # print(id1)
        current1 = DoctorSchedule.objects.filter(doctorid=id1.id,status=True)
        # print(puser)
        current=[]
        t2=datetime.today().date()
        past=[]
        for i in current1:
            if t2< i.date:
                current.append(i)
            else:
                past.append(i)

        # print(past)
        # for i in current:
        #     # slot= Slot.objects.filter(id=i.slotid)
        #     # i.slotid=slot.slot_time
        #     print(f"{i.id}, {i.patientid}, {i.doctorid.id},{i.date}, {i.slotid.slot_time}")
        if request.method=='POST':
            # print("hi")
            form_data = request.POST
            if 'actioncnl' in form_data:
                cancel_value = request.POST['actioncnl']
                # print(cancel_value,'h')
                DoctorSchedule.objects.filter(id=cancel_value).delete()
                # return HttpResponse("Success Deleted")
                return redirect("dupcoming1")
    
        else:
            return render(request,'dupcoming1.html',{"current":current})
    else:
       return HttpResponse("you are not authenticated to see this page :")
    
from django.db.models import Q
def docprescription(request):
    if request.user.is_authenticated:
        puser= ShowAppointment.objects.all()
        user= CustomUser.objects.get(id=request.user.id)
        if request.method == "POST":
            searched = request.POST['query']
            # Query The Products DB Model
            # Appointment.objects.filter(appointment_id=appointment_id)
            
            if searched.isdigit():
                print(type(searched))
                searched = ShowAppointment.objects.filter(appointment_id=searched)
            else :
                print(searched)
                searched = ShowAppointment.objects.filter( Q(date__icontains=searched))
            # Test for null
            if not searched:
                print("j")
                messages.success(request, "That Prescription Does Not Exist...Please try Again.")
                return render(request,"docpres.html",{})
            else:
                print("h",searched)
                return render(request, "docpres.html", {'searched':searched})
        # print("h:::",user.email)
        # for x in puser:
        #     print(x.appointment_id.doctorid.email,x.id)
        return render(request,"docpres.html",{'puser':puser,"user":user})
    

# views.py

from django.http import JsonResponse


def get_appointment_info(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        print(type(appointment_id),appointment_id)
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            print(appointment)
            appointment_info = {
                'patientName': appointment.patientid.first_name +" "+appointment.patientid.last_name,
                'patientAge': appointment.date,
            }
            print(appointment_info["patientName"],appointment_info["patientAge"])
            return JsonResponse(appointment_info)
        except Appointment.DoesNotExist:
            return JsonResponse({'error': 'Appointment ID not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# ////
def my_appointment(request):
    return render(request,"doctor/appointment.html")

def my_patients(request):
    return render(request,"doctor/patients.html")

from healthcare.models import Speciality
def my_profile(request):
    doctor = Doctor.objects.get(user_id = request.user.id)
    return render(request,"doctor/profile.html",{"doctor":doctor})