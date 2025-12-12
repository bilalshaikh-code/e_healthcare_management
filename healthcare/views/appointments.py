from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from healthcare.models import Appointment, DoctorSchedule

@login_required
def my_appointments(request):
    if request.user.role != 'patient':
        return redirect('home')

    today = timezone.now().date()
    upcoming = Appointment.objects.filter(patientid=request.user, date__gte=today).select_related('doctorid__user', 'slotid', 'doctorid__speciality').order_by('date')
    past = Appointment.objects.filter(patientid=request.user, date__lt=today).select_related('doctorid__user', 'slotid').order_by('-date')

    return render(request, 'patient/my_appointments.html', {
        'upcoming_appointments': upcoming,
        'past_appointments': past,
        'today': today
    })

@login_required
def cancel_appointment(request, appt_id):
    appt = get_object_or_404(Appointment, id=appt_id, patientid=request.user)
    if appt.date < timezone.now().date():
        messages.error(request, "Cannot cancel past appointments")
    else:
        appt.status = 'cancelled'
        appt.save()
        DoctorSchedule.objects.filter(doctorid=appt.doctorid, slotid=appt.slotid, date=appt.date).update(status=True)
        messages.success(request, "Appointment cancelled")
    return redirect('my_appointments')

@login_required
def appointment_history(request):
    if request.user.role != 'patient':
        return redirect('home')

    # All past appointments (completed, cancelled, no-show)
    history = Appointment.objects.filter(
        patientid=request.user,
        date__lt=timezone.now().date()
    ).select_related(
        'doctorid__user', 'slotid', 'doctorid__speciality'
    ).order_by('-date', 'slotid')

    return render(request, 'patient/appointment_history.html', {
        'history': history
    })