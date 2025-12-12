from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from healthcare.models import Appointment, Doctor, Prescription
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def doctor_appointments_view(request, period='ongoing'):
    """
    Shared view for ongoing / upcoming / past appointments
    period: 'ongoing' | 'upcoming' | 'past'
    """
    if request.user.role != 'doctor' or not request.user.doctor_profile.is_verified:
        return redirect('home')

    doctor = request.user.doctor_profile
    today = date.today()

    if period == 'ongoing':
        appointments = Appointment.objects.filter(
            doctorid=doctor,
            date__gte=today
        )
        title = "Today's & Upcoming Appointments"
    elif period == 'upcoming':
        appointments = Appointment.objects.filter(
            doctorid=doctor,
            date__gt=today
        )
        title = "Future Appointments"
    else:  # past
        appointments = Appointment.objects.filter(
            doctorid=doctor,
            date__lt=today
        )
        title = "Past Appointments"

    appointments = appointments.select_related('patientid', 'slotid', 'patientid__doctor_profile') \
                               .order_by('date', 'slotid')

    context = {
        'appointments': appointments,
        'title': title,
        'period': period,
        'today': today,
    }
    return render(request, f'doctor/appointments_{period}.html', context)


def donging(request):
    return doctor_appointments_view(request, 'ongoing')

def dupcoming(request):
    return doctor_appointments_view(request, 'upcoming')

def doutgoing(request):
    return doctor_appointments_view(request, 'past')

@login_required
def doctor_appointment_detail(request, appt_id):
    if request.user.role != 'doctor':
        return redirect('home')

    appointment = get_object_or_404(
        Appointment,
        id=appt_id,
        doctorid=Doctor.objects.get(user=request.user.id)
    )
    
    # Get prescription if exists
    try:    
        prescription = Prescription.objects.get(appointment=appointment.id)
    except Prescription.DoesNotExist:
        prescription = None

    context = {
        'appt': appointment,
        'patient': appointment.patientid,
        'prescription': prescription,
    }
    return render(request, 'doctor/appointment_detail.html', context)

@login_required
@require_POST
def mark_appointment_complete(request, appt_id):
    """
    AJAX endpoint: Doctor marks appointment as 'completed'
    """
    if request.user.role != 'doctor':
        return JsonResponse({'success=False', 'message: Unauthorized'}, status=403)

    appointment = get_object_or_404(
        Appointment,
        id=appt_id,
        doctorid=Doctor.objects.get(user=request.user.id)
    )

    # Only allow marking confirmed/pending as completed
    if appointment.status not in ['confirmed', 'pending']:
        return JsonResponse({'success': False, 'message': 'Cannot mark this appointment as completed'}, status=400)

    appointment.status = 'completed'
    appointment.save()

    # Optional: Send notification to patient
    # create_notification(appointment.patientid, "Your appointment has been completed!")

    return JsonResponse({
        'success': True,
        'message': 'Appointment marked as completed',
        'badge': '<span class="badge bg-success">Completed</span>'
    })