from django.shortcuts import render,redirect
from django.http import HttpResponse
from healthcare.models import CustomUser,Appointment, Slot, Destination
from datetime import datetime
from django.contrib import messages
from healthcare.models import ShowAppointment

def outgoing(request,):
    if request.user.is_authenticated:
        puser= CustomUser.objects.get(id=request.user.id)

        current1 = Appointment.objects.filter(patientid=puser.id)
        t2=datetime.today().date()
        past=[]
        for i in current1:
            if t2>i.date:
                past.append(i)      
        return render(request,'patient/outgoing.html',{"past":past})
    else:
       return HttpResponse("you are not authenticated to see this page :")

def ongoing(request,):
    if request.user.is_authenticated:
        puser= CustomUser.objects.get(id=request.user.id)

        current1 = Appointment.objects.filter(patientid=puser.id)
        current=[]
        t2=datetime.today().date()
        past=[]
        for i in current1:
            if t2== i.date:
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
                return redirect("ongoing")
        else:
             return render(request,'patient/ongoing.html',{"current":current})
    else:
       return HttpResponse("you are not authenticated to see this page :")
    
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
            return render(request,'patient/upcoming.html',{"current":current})
    else:
       return HttpResponse("you are not authenticated to see this page :")
    
def prescription(request):
    if request.user.is_authenticated:
        puser= ShowAppointment.objects.all()
        user= CustomUser.objects.get(id=request.user.id)
        if request.method == "POST":
            searched = request.POST['query']
            print("h::",searched)
            # Query The Products DB Model
            searched = ShowAppointment.objects.filter(appointment_id=searched)
            # searched = ShowAppointment.objects.filter(Q(date__icontains=searched))
            # Test for null
            if not searched:
                print("j")
                messages.success(request, "That Prescription Does Not Exist...Please try Again.")
                return render(request,"patient/prescription.html",{})
            else:
                print("h",searched)
                return render(request, "patient/prescription.html", {'searched':searched})
        print("h:::",user.email)
        for x in puser:
            print(x.appointment_id.patientid.email,x.id)
        return render(request,"patient/prescription.html",{'puser':puser,"user":user})