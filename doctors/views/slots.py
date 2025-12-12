from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from healthcare.models import DoctorSchedule, Appointment, Doctor
from django.contrib import messages

@login_required
def doctor_slots(request):
    if request.user.role != 'doctor' :
        return redirect('home')

    doctor = Doctor.objects.get(user=request.user.id)
    today = date.today()
    schedules = DoctorSchedule.objects.filter(doctorid=doctor).select_related('slotid').order_by('date', 'slotid')

    slots_list = []
    for sch in schedules:
        booked = Appointment.objects.filter(doctorid=doctor, slotid=sch.slotid, date=sch.date).exists()
        slots_list.append({
            'schedule': sch,
            'is_booked': booked,
            'is_upcoming': sch.date >= today,
            'patient': Appointment.objects.filter(doctorid=doctor, slotid=sch.slotid, date=sch.date).first().patientid if booked else None
        })

    if request.method == 'POST' and 'cancel_slot' in request.POST:
        sch_id = request.POST['cancel_slot']
        DoctorSchedule.objects.filter(id=sch_id, doctorid=doctor).update(status=False)
        messages.success(request, "Slot blocked")

    return render(request, 'doctor/doctor_slots.html', {'upcoming_slots': slots_list})