from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from healthcare.models import Appointment, Prescription, Doctor

@login_required
def showAppointment(request):
    if request.user.role != 'doctor':
        return redirect('home')

    if request.method == 'POST':
        appt_id = request.POST['Appointment_ID']
        appt = get_object_or_404(Appointment, id=appt_id, doctorid=Doctor.objects.get(user=request.user.id))
        
        Prescription.objects.create(
            appointment=appt,
            prescribed_by=Doctor.objects.get(user=request.user.id),
            medicines=request.POST['medicine_name'],
            dosage=request.POST.get('dosage', ''),
            instructions=request.POST.get('chat', ''),
            is_sent=True
        )
        messages.success(request, "Prescription sent!")
        return redirect('doctor_dashboard')
    appointment = None
    try:
        appt_id = request.GET.get('appt')
        appointment = Appointment.objects.get(id=appt_id)
    except:
        ...
    return render(request, 'doctor/showAppointment.html',{'appointment': appointment})

@login_required
def docprescription(request):
    prescriptions = Prescription.objects.filter(prescribed_by=request.user.doctor_profile).select_related('appointment__patientid')
    return render(request, 'doctor/docpres.html', {'puser': prescriptions})

@login_required
def get_appointment_info(request):
    if request.method == 'POST':
        appt_id = request.POST.get('appointment_id')
        try:
            appt = Appointment.objects.select_related('patientid').get(id=appt_id, doctorid=Doctor.objects.get(user=request.user.id))
            return JsonResponse({
                'patientName': appt.patientid.get_full_name(),
                'patientAge': appt.patientid.age or "N/A"
            })
        except:
            return JsonResponse({'error': 'Not found'}, status=404)
    return JsonResponse({'error': 'Invalid'}, status=400)