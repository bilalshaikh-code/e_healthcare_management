from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from healthcare.models import Appointment, DoctorSchedule, Doctor, DoctorLeave
from datetime import date, timedelta
import json
from django.http import JsonResponse

@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('home')

    doctor = request.user.doctor_profile
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday

    # ===================================================================
    # 1. Basic Stats
    # ===================================================================
    total_patients = Appointment.objects.filter(
        doctorid=doctor
    ).values('patientid').distinct().count()

    todays_appointments = Appointment.objects.filter(
        doctorid=doctor,
        date=today
    ).count()

    upcoming_appointments = Appointment.objects.filter(
        doctorid=doctor,
        date__gt=today
    ).count()

    pending_reports = Appointment.objects.filter(
        doctorid=doctor,
        date__lte=today,
        status='confirmed'
    ).exclude(prescription__isnull=False).count()  # assuming ShowAppointment = prescription

    # ===================================================================
    # 2. Upcoming Appointments Table (next 7 days)
    # ===================================================================
    appointments = Appointment.objects.filter(
        doctorid=doctor,
        date__gte=today,
        date__lte=today + timedelta(days=7)
    ).select_related('patientid', 'slotid').order_by('date', 'slotid')

    # ===================================================================
    # 3. Weekly Appointments Chart Data
    # ===================================================================
    weekly_data = []
    weekly_labels = []

    for i in range(7):
        day = start_of_week + timedelta(days=i)
        count = Appointment.objects.filter(
            doctorid=doctor,
            date=day
        ).count()
        weekly_data.append(count)
        weekly_labels.append(day.strftime("%A"))

    # ===================================================================
    # 4. Patient Age Distribution Chart
    # ===================================================================
    age_groups = {
        '0-18': 0,
        '19-35': 0,
        '36-50': 0,
        '51+': 0
    }

    patients = Appointment.objects.filter(doctorid=doctor).values('patientid__dob').distinct()
    for p in patients:
        dob = p['patientid__dob']
        if dob:
            age = (today - dob).days // 365
            if age <= 18:
                age_groups['0-18'] += 1
            elif age <= 35:
                age_groups['19-35'] += 1
            elif age <= 50:
                age_groups['36-50'] += 1
            else:
                age_groups['51+'] += 1

    age_groups_labels = list(age_groups.keys())
    age_groups_data = list(age_groups.values())

    # ===================================================================
    # 5. Notifications (Last 5 recent actions)
    # ===================================================================
    notifications = []

    # New appointments
    recent_appointments = Appointment.objects.filter(
        doctorid=doctor,
        created_at__gte=today - timedelta(days=3)
    ).select_related('patientid')[:5]

    for appt in recent_appointments:
        notifications.append({
            'message': f"New appointment with {appt.patientid.get_full_name()}",
            'timestamp': appt.created_at,
        })

    # Leaves taken
    recent_leaves = DoctorLeave.objects.filter(
        doctor=doctor,
        created_at__gte=today - timedelta(days=7)
    )[:3]

    for leave in recent_leaves:
        notifications.append({
            'message': f"Leave applied: {leave.start_date} → {leave.end_date or 'Single day'}",
            'timestamp': leave.created_at,
        })

    # Sort by timestamp
    notifications = sorted(notifications, key=lambda x: x['timestamp'], reverse=True)[:10]

    # ===================================================================
    # Context
    # ===================================================================
    context = {
        'AddDr': Doctor.objects.all(),  # for verification check in template
        'total_patients': total_patients,
        'todays_appointments': todays_appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_reports': pending_reports,

        'appointments': appointments,

        'weekly_labels': json.dumps(weekly_labels),
        'weekly_data': json.dumps(weekly_data),
        'age_groups_labels': json.dumps(age_groups_labels),
        'age_groups_data': json.dumps(age_groups_data),

        'notifications': notifications,
    }

    return render(request, 'doctor/dashboard.html', context)

@login_required
def doctor_patient(request):
    if request.user.role != 'doctor':
        return redirect('home')
    return render(request, 'doctor/patients.html')