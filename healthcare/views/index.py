from django.shortcuts import render, redirect
from healthcare.models import ContactUs, Doctor, Feedback, Speciality
from django.contrib import messages
import re
from healthcare.forms import FeedbackForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

def home(request):
    services = [
        {
            'title': 'Emergency Care',
            'description': '24/7 emergency services with rapid response team and advanced life support.',
            'icon': 'fa-ambulance'
        },
        {
            'title': 'Cardiology',
            'description': 'Complete heart care with modern cath labs, ECG, and expert cardiologists.',
            'icon': 'fa-heartbeat'
        },
        {
            'title': 'Neurology',
            'description': 'Advanced treatment for stroke, epilepsy, Parkinsons, and brain disorders.',
            'icon': 'fa-brain'
        },
        {
            'title': 'Orthopedics',
            'description': 'Joint replacement, spine surgery, sports injury, and fracture treatment.',
            'icon': 'fa-bone'
        },
        {
            'title': 'Pediatrics',
            'description': 'Complete child care from newborn to adolescence with vaccination & growth monitoring.',
            'icon': 'fa-baby'
        },
        {
            'title': 'Dermatology & Cosmetology',
            'description': 'Skin, hair, laser treatment, anti-aging, and cosmetic procedures.',
            'icon': 'fa-spa'
        },
    ]

    doctors = Doctor.objects.filter(is_verified=True)[:10]
    feedback = Feedback.objects.all()
    context = {'services': services, 'doctors': doctors, 'feedback': feedback}
    return render(request,'pages/home.html', context)

def about(request):
    doctors = Doctor.objects.filter(is_verified=True).select_related('user', 'speciality')[:12]
    specialities = Speciality.objects.all()

    return render(request, 'pages/about.html', {
        'doctors': doctors,
        'specialities': specialities,
    })

def doctor_search(request):
    doctors = Doctor.objects.filter(is_verified=True).select_related('user', 'speciality')
    specialities = Speciality.objects.all()

    # Search filters
    query = request.GET.get('q', '').strip()
    speciality_id = request.GET.get('speciality', '')

    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(speciality__name__icontains=query)
        )

    if speciality_id:
        doctors = doctors.filter(speciality_id=speciality_id)


    context = {
        'doctors': doctors,
        'specialities': specialities,
        'query': query,
        'selected_speciality': speciality_id,
        'total_doctors': doctors.count(),
    }
    return JsonResponse(context)

def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()

            messages.success(request, "Thank you! Your feedback has been submitted successfully.")
            return redirect('feedback')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Pre-fill for logged-in users
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'name': request.user.get_full_name(),
                'email': request.user.email,
            }
        form = FeedbackForm(initial=initial)

    return render(request, 'pages/feedback.html', {'form': form})

def service(request):
    services = [
        {'title': 'Cardiology', 'description': 'Advanced heart care with cath lab & expert cardiologists', 'icon': 'fa-heartbeat'},
        {'title': 'Neurology', 'description': 'Stroke treatment, EEG, migraine & brain disorder care', 'icon': 'fa-brain'},
        {'title': 'Orthopedics', 'description': 'Joint replacement, spine surgery & fracture treatment', 'icon': 'fa-bone'},
        {'title': 'Pediatrics', 'description': 'Complete child healthcare & vaccination', 'icon': 'fa-baby'},
        {'title': 'Dermatology', 'description': 'Skin, hair & cosmetic treatments', 'icon': 'fa-spa'},
        {'title': 'Emergency 24/7', 'description': 'Critical care with ambulance & ICU', 'icon': 'fa-ambulance'},
    ]
    feedback = Feedback.objects.all().order_by('-created_at')[:6]
    specialities = Speciality.objects.all()

    return render(request, 'pages/services.html', {
        'services': services,
        'feedback': feedback,
        'specialities': specialities,
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        if name != '' and email != '' and subject != '' and message != '':
            if len(name) >=3 and name.isalpha() and len(name) <= 100:
                if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',email) != None:
                    if len(subject) <= 200:
                        if len(message) <= 5000:
                            ContactUs.objects.create(
                                name=name,
                                email=email,
                                subject=subject,
                                message=message
                            )
                            messages.success(request,'Your message has been sent successfully!')
                            return redirect('contact')
                        else:
                            messages.error(request,'Message length should be 5000 characters or less.')
                            return redirect('contact')
                    else:
                        messages.error(request,'Subject length should be 200 characters or less.')
                        return redirect('contact')
                else:
                    messages.error(request,'Invalid email format.')
                    return redirect('contact')
            else:
                messages.error(request,'Name must be between 3 and 100 alphabetic characters.')
                return redirect('contact')
        else:
            messages.error(request,'Please fill all fields.')
            return redirect('contact')
    return render(request,'pages/contact.html')