from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from healthcare.models import Destination, Feedback, Doctor, ContactUs, Speciality
from django.utils import timezone
from healthcare.models import Complain, Slot, Appointment

def index(request):
    dests = Destination.objects.all()           # Pricing packages
    feedback = Feedback.objects.all()[:6]        # Latest 6 testimonials
    doctors = Doctor.objects.all()[:6]        # Show 6 doctors on homepage

    context = {
        'dests': dests,
        'feedback': feedback,
        'AddDr': doctors,       # Keep name 'AddDr' because your templates use it
    }
    return render(request, 'pages/home.html', context)


def about(request):
    doctors = Doctor.objects.all()
    return render(request, 'pages/about.html', {'AddDr': doctors})


def services(request):
    doctors = Doctor.objects.all()
    return render(request, 'pages/services.html', {'AddDr': doctors})


def pricing(request):
    packages = Destination.objects.all()  # Reuse your existing model!
    return render(request, 'pages/pricing.html', {'dests': packages})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        ContactUs.objects.create(
            name=name,
            email=email,
            subject=subject,
            msg=message
        )

        # Send email
        try:
            send_mail(
                subject=f"New Contact: {subject}",
                message=f"From: {name} ({email})\n\nMessage:\n{message}",
                from_email=email,
                recipient_list=['tirth5524@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, f"Thank you {name}! We received your message.")
        except Exception as e:
            messages.error(request, "Message saved but email failed. We'll contact you soon.")

        return redirect('contact')  # Redirect to avoid re-submission

    return render(request, 'pages/contact.html')


# Dynamic Service Detail (Already Fixed)
def service_detail(request, service_id):
    SERVICES = [
        {"id": 1, "name": "Emergency Care", "tagline": "24/7 Life-Saving Response", "hero_img": "img/emergency-hero.jpg", "image": "img/emergency.jpg", "description": "Our Level 1 Trauma Center operates 24/7...", "features": ["24/7 Emergency", "Helicopter Service", "100+ ICU Beds"]},
        {"id": 2, "name": "Operation & Surgery", "tagline": "Advanced Surgical Excellence", "hero_img": "img/surgery-hero.jpg", "image": "img/surgery.jpg", "description": "Robotic and minimally invasive surgery...", "features": ["Robotic Surgery", "Expert Team"]},
        {"id": 3, "name": "Outdoor Checkup", "tagline": "Health Screening at Your Doorstep", "hero_img": "img/checkup-hero.jpg", "image": "img/checkup.jpg", "description": "We bring health checkups to you...", "features": ["Home Visits", "Full Checkup"]},
        {"id": 4, "name": "Ambulance Service", "tagline": "Free & Fast Medical Transport", "hero_img": "img/ambulance-hero.jpg", "image": "img/ambulance.jpg", "description": "Free 24/7 ambulance service...", "features": ["100% Free", "GPS Tracked"]},
        {"id": 5, "name": "Medicine & Pharmacy", "tagline": "Genuine Medicines 24/7", "hero_img": "img/pharmacy-hero.jpg", "image": "img/pharmacy.jpg", "description": "In-house pharmacy open 24/7...", "features": ["24/7 Open", "Home Delivery"]},
        {"id": 6, "name": "Blood Testing & Lab", "tagline": "Accurate Results in Hours", "hero_img": "img/lab-hero.jpg", "image": "img/lab.jpg", "description": "NABL-accredited lab...", "features": ["1000+ Tests", "Fast Reports"]},
    ]

    service = next((s for s in SERVICES if s["id"] == service_id), None)
    if not service:
        from django.http import Http404
        raise Http404("Service not found")

    return render(request, "pages/service_detail.html", {"service": service})

def appointment(request):
    if request.method == 'POST':
        try:
            # Get current logged-in user
            patient = request.user  # Already authenticated → use directly

            speciality_id = request.POST.get('speciality')
            doctor_id = request.POST.get('doctor')
            patient_name = request.POST.get('patient')
            email = request.POST.get('email')
            date = request.POST.get('date')
            time_slot_id = request.POST.get('time')

            # Basic validation
            if not all([speciality_id, doctor_id, date, time_slot_id]):
                messages.error(request, "Please fill all fields.")
                return redirect('appointment')

            # Get objects
            doctor = Doctor.objects.get(id=doctor_id)
            slot = Slot.objects.get(id=time_slot_id)

            # Prevent booking past dates
            if date < str(timezone.now().date()):
                messages.error(request, "Cannot book appointment for past date.")
                return redirect('appointment')

            # Check if doctor has less than 11 appointments on that date
            existing_count = Appointment.objects.filter(
                doctorid=doctor,
                date=date
            ).count()

            if existing_count >= 11:
                messages.error(request, f"Dr. {doctor.username} is fully booked on {date}. Please choose another date.")
                return redirect('appointment')

            # Create appointment
            appointment = Appointment.objects.create(
                patientid=patient,
                doctorid=doctor,
                slotid=slot,
                date=date,
                status="pending"
            )

            messages.success(request, f"Appointment booked successfully with Dr. {doctor.username} on {date} at {slot.slot_time}!")
            # return paymentinvoice(request, appointment)  # Redirect to payment

        except Doctor.DoesNotExist:
            messages.error(request, "Selected doctor not found.")
        except Slot.DoesNotExist:
            messages.error(request, "Selected time slot is no longer available.")
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")

        return redirect('appointment')

    else:
        # GET request → show form
        specialities = Speciality.objects.all()  # Your specialty model
        return render(request, 'pages/appointment/view.html', {
            'speciality': specialities,
        })

def complain(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('patientname', '').strip()
            email = request.POST.get('email', '').strip()
            msg = request.POST.get('complain', '').strip()

            # Basic validation
            if not all([name, email, msg]):
                messages.error(request, "All fields are required.")
                return redirect('complain')

            # Save complaint to database
            Complain.objects.create(
                patient_name=name,
                email=email,
                complain_message=msg
            )

            # Send email to admin
            subject = f"New Complaint from {name}"
            message = f"""
New Complaint Received:

Name: {name}
Email: {email}

Message:
{msg}

---
HealthPlus Hospital Complaint System
            """
            send_mail(
                subject=subject,
                message=message,
                from_email=email,  # or settings.DEFAULT_FROM_EMAIL
                recipient_list=['tirth5524@gmail.com'],  # your admin email
                fail_silently=False,
            )

            messages.success(request, "Thank you! Your complaint has been submitted successfully. We will contact you soon.")
            return redirect('complain')  # Redirect to avoid form resubmission

        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
            print(f"Complaint error: {e}")  # For debugging

    # GET request → show form
    return render(request, 'pages/complain.html')

def feedback(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('pname', '').strip()
            email = request.POST.get('email', '').strip()
            message = request.POST.get('message', '').strip()
            rating = request.POST.get('rating', '0')  # from star rating

            # Validation
            if not all([name, email, message, rating.isdigit()]):
                messages.error(request, "Please fill all fields correctly.")
                return redirect('feedback')

            # Save to database
            Feedback.objects.create(
                p_name=name,
                email=email,
                rate=int(rating),
                message=message
            )

            # Optional: Send email to admin
            send_mail(
                subject=f"New Feedback ({rating}/5) from {name}",
                message=f"""
New Feedback Received!

Name: {name}
Email: {email}
Rating: {rating}/5 stars

Message:
{message}

---
HealthPlus Hospital Feedback System
                """,
                from_email=email,
                recipient_list=['tirth5524@gmail.com'],  # Your admin email
                fail_silently=False,
            )

            messages.success(request, "Thank you! Your feedback has been submitted successfully.")
            return redirect('feedback')  # Redirect to prevent resubmission

        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
            print(f"Feedback error: {e}")

    # GET request → show form
    return render(request, 'pages/feedback.html')