from datetime import datetime
from django.http import HttpResponse
from .models import Destination
from django.shortcuts import render
import profile
import uuid
from django.contrib import messages
from django.shortcuts import redirect, render
# from django.contrib.auth.models import User 
from .models import CustomUser
# from django.contrib.auth import authenticate 
from django.contrib import auth
# from django.contrib.auth import get_user_model
# from newww.project.typro.account1.forms import register1
# from .helper import send_forget_password_mail
from .models import *
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import UserProfileForm
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse
from django.http import JsonResponse

# Create your views here.
def get_doctors(request):
    specialty_id = request.GET.get('specialty_id')
    doctors = Doctor.objects.filter(speciality = specialty_id).values('id','user','speciality')
    for doctor in doctors:
        doctor['user'] = CustomUser.objects.get(id=doctor['user']).get_full_name()
        doctor['speciality'] = Speciality.objects.get(id=doctor['speciality']).name
    return JsonResponse(list(doctors), safe=False)

def get_slots(request):
    selectedDate= request.GET.get('selectedDate')
    docId  = request.GET.get('doctorId')
    print(type(docId))
    docId1=docId
    if docId1.isdigit():
       docId=docId1
    else:
       print("h",docId1)
       words = docId1.split()
       print(words)
       docId=Doctor.objects.get(firstName=words[0])
    slot1=[]
    slots=[]
    # print(docId)
    slot = DoctorSchedule.objects.filter(date=selectedDate,doctorid=docId,status=True).values('slotid')
    print("hi 1",slot)
    for i in slot:
        # print("k",i)
        for key,value  in i.items():
            if Appointment.objects.filter(date=selectedDate,slotid=value,doctorid=docId,status="Success").count()<=1:
                slot1.append(Slot.objects.filter(id = value).values('id','slot_time'))
    # print("hi",slot)
    for m in slot1:
        for n in m:
            slots.append(n)
    return JsonResponse(list(slots), safe=False)

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# RZP_API_KEY='rzp_test_HbVeg2ZkY2GmUI'
# RZP_API_SECRET='zjFcPssv4soJgmMOgqnFAfW1'
# razorpay_pay_order_id= models.CharField(max_length=100,null=True,blank=True)
#     razorpay_pay_payment_id= models.CharField(max_length=100,null=True,blank=True)
#     razorpay_pay_signature_id= models.CharField(max_length=100,null=True,blank=True)
def paymentinvoice(request,book_appointment):
    if request.user.is_authenticated:
        amount =int(book_appointment.doctorid.fees*100) 
        client=razorpay.Client(auth=(settings.RZP_API_KEY,settings.RZP_API_SECRET))
        payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        pi= Payment.objects.create(appointment_id=book_appointment,fees=book_appointment.doctorid.fees,razorpay_pay_order_id=payment['id'])
        # book_appointment.status="Success"
        # book_appointment.save()
        print(book_appointment)
        global xmail,bstatus,pid
        xmail = book_appointment.patientid.email
        bstatus=book_appointment
        pid=pi
    print("hi:",Payment)
    context={'cart':book_appointment,'payment':payment}
    return render(request,'paymentinvoice.html',{'book_appointment':book_appointment,'context':context,'amount':amount}) 

@csrf_exempt
def OrderSuccess(request):
    print("payment")
    e="tirth5524@gmail.com"
    bstatus.status="Success"
    bstatus.save()
    subject = 'Appointment Booking Conformation'
    # message="Success"
    # message += f'\n----------------------------------------------------------------------'
    # message += f'\n\n Thank uou,\n Regards HealthPlus'
    message=f"""
        Subject: Payment Receipt for Appointment Booking
        Dear {pid.appointment_id.patientid.first_name} {pid.appointment_id.patientid.last_name},
        Thank you for booking your appointment with us. Your payment has been successfully processed, and we're excited to confirm your appointment details:

        Appointment ID:{pid.appointment_id.id}
        Appointment Date: {pid.appointment_id.date}
        Appointment Time: {pid.appointment_id.slotid.slot_time}
        Doctor Name:Dr.{pid.appointment_id.doctorid}
        Amount Paid: {pid.fees}

        

        If you have any questions or need further assistance, feel free to contact us.

        We look forward to seeing you on {pid.appointment_id.date}.

        Best regards,
        [HealthPlus]
        """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [e,xmail]
    send_mail(subject, message, email_from, recipient_list)
    return render(request,"paymentsuccess.html")

# def paymentinvoice1(request):
           
#             # message = "The Selected Doctor Slot Is Full! The Selected Day Is Full!"
#             # return HttpResponse(message)
#             return render(request,'paymentinvoice.html') 
    
# def place_order_online(request):
#     if request.session.has_key('customer_id'):
#         uid = request.session['customer_id']
#         ca = Booking.objects.filter(Customer_id_id=uid)
#         for data in ca:
#             ph_id = data.Photographer_id_id
#             pk_id = data.Package_id_id
#             da = data.Datetime
#             total = data.Total_cost
    
#         o = Booking(Customer_id_id=uid, Photographer_id_id=ph_id ,Package_id_id=pk_id,Datetime=da,Total_cost=total, Booking_Status=0, Payment_status=1)
#         o.save()
#         id = Booking.objects.latest('Booking_id')
#         print('------------------------------booking id in online',id)
#         c = Booking.objects.filter(Customer_id_id=uid)
#         c1 =  Booking.objects.filter(Customer_id_id=uid).count()
#         if c1 >= 1:
#             e = request.session['Email']
#             obj = Customer.objects.filter(Email=e).count()
#             val = Customer.objects.get(Email=e)
#             if obj == 1:
#                 ord1 = Booking.objects.filter(Booking_id=id.Booking_id)
#                 subject = 'Booking Conformation'
#                 message = f'Dear {val.F_name} {val.L_name}, \n\n\t ' \
#                         f'Package details are as follows:'
#                 message += f'\n---------------------------------------------------------------------'
#                 message += f'\n  Package name'
#                 message += f'\n----------------------------------------------------------------------'
#                 for data in ord1:
#                     print("---------------------------------", data)
#                     message += f'\n {data.Package_id.Package_name}'
#                 message += f'\n----------------------------------------------------------------------'
#                 message += f'\n  Total \t\t\t {total}'
#                 message += f'\n----------------------------------------------------------------------'
#                 message += f'\n\n Thank uou,\n Regards 4 Focus Photography'
#                 email_from = settings.EMAIL_HOST_USER
#                 recipient_list = [e, ]
#                 send_mail(subject, message, email_from, recipient_list)
#         else:
#             messages.error(request, "You don't have any product in your Cart!")
#             return render(request, "checkout.html")
#         return redirect("/Customer/indux/")
#     return render(request, 'checkout.html')

def upcoming(request):

    if request.user.is_authenticated:
        puser= CustomUser.objects.get(id=request.user.id)

        current1 = Appointment.objects.filter(patientid=puser.id)
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
            print("form:",form_data)
            if 'actioncnl' in form_data:
                cancel_value = request.POST['actioncnl']
                # print(cancel_value,'h')
                Appointment.objects.filter(id=cancel_value).delete()
                # return HttpResponse("Success Deleted")
                return redirect("upcoming")
            elif 'actioncno' in form_data:
                update_value = request.POST['actioncno']
                u=Appointment.objects.get(id=update_value)
                print(u.doctorid.speciality)
                global xyu
                xyu=u
                print(xyu)
                speciality=Destination.objects.all()
                slots=Slot.objects.all()
                # updateAppointment(request,u)
                # return redirect("updateAppointment")
                return render(request,'updateAppointment.html',{'slots':slots,'speciality':speciality,"u":u})
    
        else:
            return render(request,'upcoming.html',{"current":current})
    else:
       return HttpResponse("you are not authenticated to see this page :")
# def getss():
#     return xyu
def updateAppointment(request):
    u=xyu
    print(u)
    hhh=Appointment.objects.get(id=u.id)
    print(hhh)
    if request.method=='POST':
            if request.user.is_authenticated:
                puser= CustomUser.objects.get(id=request.user.id)
                speciality_id = request.POST.get('speciality')
                doctor_id = request.POST.get('doctor')
                patient_name = request.POST.get('patient')
                email = request.POST.get('email')
                date = request.POST.get('date')
                time = request.POST.get('time')

                
                print("hello",speciality_id," ",doctor_id,"  hi",type(doctor_id)," ",patient_name," ",email," ",date," ",time)
                doctor_id1=doctor_id
                print(type(doctor_id))
                if type(doctor_id1) is str:
                    print("h",doctor_id1)
                    words = doctor_id1.split()
                    print(words)
                    
                    doctor_id=Doctor.objects.get(firstName=words[0],lastName=words[1])
                    print(doctor_id.id)
                    
                print(puser)
                # if puser is request.user.email:
                #     puser=CustomUser.objects.get(email=request.user.email)
                sid=Slot.objects.get(id=time)
                did=Doctor.objects.get(id=doctor_id.id)
                # patient = CustomUser.objects.get(email=email) 
                # date1=datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")
                print("mail",puser,"id :",puser.id,"type :",type(puser))

                # time1 = str(datetime.today().date())
                # if date1 < time1:
                #     return HttpResponse("You Have Selected Wrong Date Please Select Valid Date ")
                
                # book_appointment= Appointment.objects.create(
                #     patientid=patient,
                #     doctorid=did,
                #     slotid=sid,
                #     date=date1
                # )
                
                if Appointment.objects.filter(date=date,doctorid=did).count()<11:
                            
                            hhh.patientid=puser
                            hhh.doctorid=did
                            hhh.slotid=sid
                            hhh.date=date
                            hhh.save()
                            return redirect("upcoming")
                else :
                        print("hi 1")
                        messages.info(request, "The Selected Doctor Slot Is Full! The Selected Day Is Full!")
                        message = "The Selected Doctor Slot Is Full! The Selected Day Is Full!"
                        return HttpResponse(message)
            else:
                # redirect("/")
                return HttpResponse("Please Login First Then Book Appointment :")
                
                

                # speciality=Destination.objects.all()
                # slots=Slot.objects.all(){'slots':slots,'speciality':speciality}
            
    
    else :
            speciality=Destination.objects.all()
            slots=Slot.objects.all()
            # print("hey",xyu.doctorid)
            # hu=Appointment.objects.get(id=xyu.id)
            # u=getss()
            print("hi",u)
            # print(xyu)
            return render(request,'updateAppointment.html',{'slots':slots,'speciality':speciality,"u":u})
    
def email_exists(email):
    return Doctor.objects.filter(email=email).exists()