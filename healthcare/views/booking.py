# healthcare/views/patient/booking.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from datetime import date
from django.contrib import messages
from healthcare.models import Doctor, DoctorSchedule, Slot, Appointment, DoctorLeave

@login_required
def book_appointment(request):
    if request.user.role != 'patient':
        return redirect('home')
    doctors = Doctor.objects.filter(is_verified=True).select_related('user', 'speciality')
    return render(request, 'patient/book_appointment.html', {'doctors': doctors})

@require_http_methods(["GET"])
def get_available_slots(request):
    doctor_id = request.GET.get('doctor')
    date_str = request.GET.get('date')
    if not doctor_id or not date_str:
        return JsonResponse({'error': 'Missing params'}, status=400)

    try:
        sel_date = date.fromisoformat(date_str)
        doctor = Doctor.objects.get(id=doctor_id)
        schedules = DoctorSchedule.objects.filter(doctorid=doctor, date=sel_date).select_related('slotid')

        slots = []
        for sch in schedules:
            booked = Appointment.objects.filter(doctorid=doctor, slotid=sch.slotid, date=sel_date).exists()
            slots.append({
                'id': sch.slotid.id,
                'time': sch.slotid.slot_time,
                'available': sch.status and not booked
            })

        return JsonResponse({
            'slots': slots,
            'fees': doctor.fees,
            'doctor_name': f"Dr. {doctor.user.get_full_name()}"
        })
    except:
        return JsonResponse({'error': 'Invalid data'}, status=400)

@login_required
def confirm_booking(request):
    if request.method == "POST":
        doctor = get_object_or_404(Doctor, id=request.POST['doctor_id'])
        slot = get_object_or_404(Slot, id=request.POST['slot_id'])
        appt_date = date.fromisoformat(request.POST['date'])

        # Prevent double booking
        if Appointment.objects.filter(doctorid=doctor, slotid=slot, date=appt_date).exists():
            messages.error(request, "Slot already booked!")
            return redirect('book_appointment')

        Appointment.objects.create(
            patientid=request.user,
            doctorid=doctor,
            slotid=slot,
            date=appt_date,
            symptoms=request.POST.get('symptoms', ''),
            status='confirmed'
        )
        # Mark slot as booked
        DoctorSchedule.objects.filter(doctorid=doctor, slotid=slot, date=appt_date).update(status=False)

        messages.success(request, "Appointment booked!")
        return redirect('my_appointments')

    return redirect('book_appointment')