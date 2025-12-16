from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from healthcare.models import Appointment

@login_required(login_url="login")
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('home')

    today = timezone.now().date()
    appointments = Appointment.objects.filter(patientid=request.user).select_related('doctorid', 'slotid')

    context = {
        'total_appointments': appointments.count(),
        'upcoming_count': appointments.filter(date__gte=today).count(),
        'completed_count': appointments.filter(date__lt=today, status='completed').count(),
        'prescription_count': appointments.filter(prescription__isnull=False).count(),
        'upcoming_appointments': appointments.filter(date__gte=today).order_by('date', 'slotid')[:5],
        'latest_prescription': appointments.filter(prescription__isnull=False).first(),
    }
    return render(request, 'patient/dashboard.html', context)