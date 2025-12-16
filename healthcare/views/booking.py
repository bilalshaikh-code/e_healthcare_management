# healthcare/views/patient/booking.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from datetime import date
from django.contrib import messages
from healthcare.models import Doctor, DoctorSchedule, Slot, Appointment, ChatRoom
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@login_required(login_url="login")
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

@login_required(login_url="login")
def confirm_booking(request):
    if request.method == "POST":
        doctor = get_object_or_404(Doctor, id=request.POST['doctor_id'])
        slot = get_object_or_404(Slot, id=request.POST['slot_id'])
        appt_date = date.fromisoformat(request.POST['date'])

        # Prevent double booking
        if Appointment.objects.filter(doctorid=doctor, slotid=slot, date=appt_date).exists():
            messages.error(request, "Slot already booked!")
            return redirect('book_appointment')

        appointment = Appointment.objects.create(
            patientid=request.user,
            doctorid=doctor,
            slotid=slot,
            date=appt_date,
            symptoms=request.POST.get('symptoms', ''),
            status='confirmed'
        )
        # After Appointment.objects.create(...)
        ChatRoom.objects.get_or_create(
            patient=request.user,
            doctor=appointment.doctorid,
            appointment=appointment,
            defaults={'is_active': True}
        )

        # SEND CONFIRMATION EMAIL
        context = {
            'patient': request.user,
            'appointment': appointment,
        }
        html_message = render_to_string('emails/appointment_confirmation.html', context)
        plain_message = f"Appointment confirmed with Dr. {doctor.user.get_full_name()} on {appt_date} at {slot.slot_time}"

        send_mail(
            subject=f"Appointment Confirmed - #{appointment.id}",
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            html_message=html_message,
            fail_silently=False,
        )

        # Optional: Notify doctor too
        send_mail(
            "New Appointment",
            f"New appointment from {request.user.get_full_name()} on {appt_date} {slot.slot_time}",
            settings.DEFAULT_FROM_EMAIL,
            [doctor.user.email],
        )

        # Mark slot as booked
        DoctorSchedule.objects.filter(doctorid=doctor, slotid=slot, date=appt_date).update(status=False)

        messages.success(request, "Appointment booked & confirmation email sent!")
        return redirect('my_appointments')

    return redirect('book_appointment')