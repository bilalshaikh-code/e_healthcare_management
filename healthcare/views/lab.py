# views/patient/lab.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime
from healthcare.models import LabTest, LabTestCategory, LabBooking

@login_required
def lab_test_booking(request):
    if request.user.role != 'patient':
        return redirect('home')

    categories = LabTestCategory.objects.filter(is_active=True).prefetch_related('tests')

    if request.method == 'POST':
        selected_tests = request.POST.getlist('tests')
        date = request.POST['date']
        time = request.POST['time']
        notes = request.POST.get('notes', '')

        if not selected_tests:
            messages.error(request, "Please select at least one test.")
            return redirect('lab_test_booking')

        tests = LabTest.objects.filter(id__in=selected_tests)
        total = sum(test.price for test in tests)

        booking = LabBooking.objects.create(
            patient=request.user,
            appointment_date=date,
            appointment_time=time,
            total_amount=total,
            notes=notes
        )
        booking.tests.set(tests)
        booking.save()

       # In your lab_booking view — add this before render/email
        has_fasting_tests = any(test.fasting_required for test in tests)

        # In context:
        context = {
            'patient': request.user,
            'booking': booking,
            'tests': tests,
            'has_fasting_tests': has_fasting_tests,  # ← Add this line
        }
        html_message = render_to_string('emails/lab_booking_confirmation.html', context)
        plain_message = render_to_string('emails/lab_booking_confirmation.txt', context)

        send_mail(
            subject=f"Lab Test Booking Confirmed - #{booking.id}",
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            html_message=html_message,
            fail_silently=False,
        )

        # Optional: Email to lab admin
        send_mail(
            "New Lab Booking",
            f"New booking from {request.user.get_full_name()} for {date} {time}",
            settings.DEFAULT_FROM_EMAIL,
            ['lab@healthplus.com'],
        )

        messages.success(request, f"Lab tests booked! Total: ₹{total}")
        return redirect('lab_booking_success')

    return render(request, 'patient/lab_booking.html', {
        'categories': categories
    })

def lab_booking_success(request):
    if request.user.role != 'patient':
        return redirect('home')

    # Get the latest booking
    try:
        booking = LabBooking.objects.filter(patient=request.user).latest('created_at')
    except LabBooking.DoesNotExist:
        return redirect('lab_test_booking')

    # Check if any test requires fasting
    has_fasting_tests = booking.tests.filter(fasting_required=True).exists()

    return render(request, 'patient/lab_booking_success.html', {
        'booking': booking,
        'has_fasting_tests': has_fasting_tests,  # ← This fixes the error!
    })