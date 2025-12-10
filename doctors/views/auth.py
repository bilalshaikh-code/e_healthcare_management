from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import DoctorRegisterForm
from healthcare.models import CustomUser, Doctor

def register(request):
    if request.method == "POST":
        form = DoctorRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.role = "doctor"
            user.save()

            # Create doctor profile
            Doctor.objects.create(
                user=user,
                dob=form.cleaned_data["dob"],
                gender=form.cleaned_data["gender"],
                degree=form.cleaned_data["degree"],
                speciality=form.cleaned_data["speciality"],
                fees=form.cleaned_data["fees"],
            )

            # messages.success(request, "Registration successful! Wait for admin approval.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DoctorRegisterForm()
    return render(request, "auth/doctor/register.html", {"form": form})
