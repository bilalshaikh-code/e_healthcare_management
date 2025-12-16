from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url="login")
def patient_profile(request):
    if request.user.role != 'patient':
        return redirect('home')

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.mobile_number = request.POST['mobile_number']
        user.dob = request.POST.get('dob') or None
        user.gender = request.POST.get('gender')
        user.address = request.POST.get('address', '')
        if request.FILES.get('image'):
            user.image = request.FILES['image']
        user.save()
        messages.success(request, "Profile updated!")
        return redirect('patient_profile')

    return render(request, 'patient/profile.html')