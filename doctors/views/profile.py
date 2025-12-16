# healthcare/views/doctor/profile.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from healthcare.models import Appointment, Prescription

@login_required(login_url="login")
def doctor_profile(request):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied.")
        return redirect('home')

    doctor = request.user.doctor_profile

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            # Update profile
            request.user.first_name = request.POST['first_name'].strip()
            request.user.last_name = request.POST.get('last_name', '').strip()
            request.user.mobile_number = request.POST['mobile_number']
            doctor.degree = request.POST['degree']
            doctor.experience_years = request.POST['experience_years']
            doctor.fees = request.POST['fees']
            if request.FILES.get('image'):
                request.user.image = request.FILES['image']
            request.user.save()
            doctor.save()
            messages.success(request, "Profile updated successfully!")

        elif action == 'change_password':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, "Password changed successfully!")
            else:
                for error in form.errors.values():
                    messages.error(request, error)

        elif action == 'delete_account':
            if request.POST.get('confirm_delete') == 'DELETE':
                with transaction.atomic():
                    request.user.delete()
                messages.success(request, "Your account has been permanently deleted.")
                return redirect('login')
            else:
                messages.error(request, "Type 'DELETE' to confirm.")

        return redirect('doctor_profile')

    # Stats
    total_patients = Appointment.objects.filter(doctorid=doctor).values('patientid').distinct().count()
    total_appointments = Appointment.objects.filter(doctorid=doctor).count()
    total_prescriptions = Prescription.objects.filter(prescribed_by=doctor).count()

    password_form = PasswordChangeForm(request.user)

    return render(request, 'doctor/profile.html', {
        'doctor': doctor,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_prescriptions': total_prescriptions,
        'password_form': password_form,
    })