from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import date, timedelta
from healthcare.models import DoctorWeeklySchedule, Doctor, DoctorLeave, DoctorSchedule, Slot, Appointment

@login_required
def weekly_schedule(request):
    if request.user.role != 'doctor':
        return redirect('home')
    
    doctor = Doctor.objects.get(user=request.user.id)

    if request.method == 'POST':
        DoctorWeeklySchedule.objects.filter(doctor=doctor).delete()
        days = request.POST.getlist('days')
        slots = request.POST.getlist('slots')
        for day in days:
            for slot_id in slots:
                DoctorWeeklySchedule.objects.create(doctor=doctor, day_of_week=day, slot_id=slot_id)
        messages.success(request, "Weekly schedule saved!")
        return redirect('weekly_schedule')

    slots = Slot.objects.all()
    current_rules = DoctorWeeklySchedule.objects.filter(doctor=doctor).select_related('slot')

    return render(request, 'doctor/weekly_schedule.html', {
        'slots': slots,
        'current_rules': current_rules,
        'days': ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    })

@login_required
def take_leave(request):
    if request.user.role != 'doctor':
        return redirect('home')
    
    doctor = Doctor.objects.get(user=request.user.id)

    if request.method == 'POST':
        start = request.POST['start_date']
        end = request.POST.get('end_date') or start
        reason = request.POST.get('reason', 'Personal')
        DoctorLeave.objects.create(doctor=doctor, start_date=start, end_date=end, reason=reason)
        messages.success(request, "Leave applied!")
        return redirect('take_leave')

    leaves = DoctorLeave.objects.filter(doctor=doctor).order_by('-start_date')
    return render(request, 'doctor/take_leave.html', {'leaves': leaves})

@login_required
def doctor_calendar(request):
    if request.user.role != 'doctor':
        return redirect('home')
    
    doctor = Doctor.objects.get(user=request.user.id)

    # Optional: Check if doctor has any slots (for empty state)
    has_slots = DoctorSchedule.objects.filter(doctorid=doctor).exists()
    has_leave = DoctorLeave.objects.filter(doctor=doctor).exists()

    context = {
        'doctor': doctor,
        'has_slots': has_slots or has_leave,
    }
    return render(request, 'doctor/calendar.html', context)

@login_required
def calendar_events_api(request):
    if request.user.role != 'doctor':
        return JsonResponse([])
    doctor = Doctor.objects.get(user=request.user.id)
    events = []
    # Available slots (green)
    available = DoctorSchedule.objects.filter(
        doctorid=doctor,
        status=True,
        date__gte=date.today()
    ).select_related('slotid').values('date', 'slotid__slot_time')[:200]

    for slot in available:
        events.append({
            'title': slot['slotid__slot_time'],
            'start': slot['date'].isoformat(),
            'color': '#28a745',  # green
            'textColor': 'white',
            'isLeave': False
        })

    # Leave dates (red)
    leaves = DoctorLeave.objects.filter(doctor=doctor)
    for leave in leaves:
        current = leave.start_date
        end = leave.end_date or leave.start_date
        while current <= end:
            events.append({
                'title': 'Leave - ' + (leave.reason or 'Personal'),
                'start': current.isoformat(),
                'end': (f"{current.year}-{current.month}-{current.day + 1}") if current != end else None,
                'allDay': True,
                'color': '#dc3545',
                'textColor': 'white',
                'isLeave': True,
                'reason': leave.reason
            })
            current += timedelta(days=1)

    return JsonResponse(events, safe=False)