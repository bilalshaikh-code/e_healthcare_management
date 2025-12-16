from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from healthcare.models import CustomUser, Doctor, Speciality

def register(request):
    if request.method == "POST":
        email = request.POST['email'].strip().lower()
        password = request.POST['password']
        password2 = request.POST['password2']
        role = request.POST['role']
        first_name = request.POST['first_name'].strip()
        mobile = request.POST['mobile_number']

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect('register')

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            mobile_number=mobile,
            role=role
        )

        if role == 'doctor':
            Doctor.objects.create(
                user=user,
                degree=request.POST.get('degree', ''),
                speciality_id=request.POST.get('speciality'),
                fees=request.POST.get('fees', 500),
                is_verified=False
            )
            messages.success(request, "Doctor account created! Waiting for admin approval.")
            login(request, user)
            return redirect('doctor_dashboard' if role == 'doctor' else 'home')
        else:
            messages.success(request, "Welcome! You can now log in.")

        login(request, user)
        return redirect('patient_dashboard' if role == 'patient' else 'home')

    specialities = Speciality.objects.all()
    return render(request, 'auth/register.html', {'specialities': specialities})


def login_view(request):
    if request.method == "POST":
        email = request.POST['email'].strip().lower()
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            if user.role == 'patient':
                return redirect('patient_dashboard')
            elif user.role == 'doctor':
                if Doctor.objects.get(user=user.id).is_verified:
                    return redirect('doctor_dashboard')
                else:
                    messages.warning(request, "Your doctor account is pending approval.")
                    return redirect('home')
            else:
                return redirect('/admin/')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')


# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'emails/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'