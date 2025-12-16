# views/patient/rating.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from healthcare.models import Appointment, DoctorReview

@login_required(login_url="login")
def rate_doctor(request, appointment_id):
    if request.user.role != 'patient':
        return redirect('home')

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patientid=request.user,
        status='completed'  # Only completed appointments
    )

    # Prevent double rating
    if DoctorReview.objects.filter(appointment=appointment).exists():
        messages.info(request, "You have already rated this appointment.")
        return redirect('my_appointments')

    if request.method == 'POST':
        rating = int(request.POST['rating'])
        comment = request.POST.get('comment', '')

        DoctorReview.objects.create(
            doctor=appointment.doctorid,
            patient=request.user,
            appointment=appointment,
            rating=rating,
            comment=comment
        )
        messages.success(request, "Thank you! Your rating has been recorded.")
        return redirect('my_appointments')

    return render(request, 'patient/rate_doctor.html', {
        'appointment': appointment,
        'doctor': appointment.doctorid
    })