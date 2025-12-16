# python manage.py shell
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from datetime import datetime, time, date, timedelta
from healthcare.models import *

print("Creating demo data for HealthPlus Hospital...")

# 1. Create Specialities
specialities = [
    "Cardiology", "Neurology", "Pediatrics", "Orthopedics", "Dermatology",
    "Gynecology", "General Medicine", "ENT", "Ophthalmology", "Psychiatry"
]
for name in specialities:
    Speciality.objects.get_or_create(name=name)

# 2. Create Time Slots
slots = [
    ("09:00 AM - 09:30 AM", "09:00", "09:30"),
    ("09:30 AM - 10:00 AM", "09:30", "10:00"),
    ("10:00 AM - 10:30 AM", "10:00", "10:30"),
    ("10:30 AM - 11:00 AM", "10:30", "11:00"),
    ("11:00 AM - 11:30 AM", "11:00", "11:30"),
    ("11:30 AM - 12:00 PM", "11:30", "12:00"),
    ("02:00 PM - 02:30 PM", "14:00", "14:30"),
    ("02:30 PM - 03:00 PM", "14:30", "15:00"),
    ("03:00 PM - 03:30 PM", "15:00", "15:30"),
    ("04:00 PM - 04:30 PM", "16:00", "16:30"),
    ("04:30 PM - 05:00 PM", "16:30", "17:00"),
    ("05:00 PM - 05:30 PM", "17:00", "17:30"),
]
for slot_time, start, end in slots:
    Slot.objects.get_or_create(
        slot_time=slot_time,
        defaults={'start_time': start, 'end_time': end}
    )

# 3. Create Admin
admin_user, _ = CustomUser.objects.get_or_create(
    email='admin@healthplus.com',
    defaults={
        'first_name': 'Super',
        'last_name': 'Admin',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
        'password': make_password('admin123'),
    }
)

# 4. Create 8 Verified Doctors
doctors_data = [
    ("Dr. Rajesh Sharma", "Cardiology", "MBBS, MD, DM", 15, 800),
    ("Dr. Priya Patel", "Neurology", "MBBS, MD, DM", 12, 900),
    ("Dr. Amit Kumar", "Pediatrics", "MBBS, DCH", 10, 600),
    ("Dr. Neha Gupta", "Dermatology", "MBBS, DVD", 8, 700),
    ("Dr. Vikram Singh", "Orthopedics", "MBBS, MS", 18, 1000),
    ("Dr. Anjali Desai", "Gynecology", "MBBS, DGO", 14, 750),
    ("Dr. Rohan Mehta", "General Medicine", "MBBS, MD", 11, 650),
    ("Dr. Sneha Reddy", "ENT", "MBBS, MS", 9, 700),
]

for name, spec, degree, exp, fees in doctors_data:
    first, last = name.split(" ", 1)
    email = f"{first.lower()}.{last.lower()}@healthplus.com".replace(" ", "")
    
    user = CustomUser.objects.create(
        email=email,
        first_name=first,
        last_name=last,
        role='doctor',
        mobile_number=f"98{str(hash(email))[-8:]}",
        password=make_password('doctor123'),
        is_active=True
    )
    
    doctor = Doctor.objects.create(
        user=user,
        speciality=Speciality.objects.get(name=spec),
        degree=degree,
        experience_years=exp,
        fees=fees,
        consultation_time=30,
        is_verified=True,
        rating=4.8,
        total_reviews=127
    )

# 5. Create 10 Patients
patients = [
    ("Aarav Patel", "aarav@gmail.com", "9876543210"),
    ("Isha Sharma", "isha@gmail.com", "9876543211"),
    ("Vihaan Singh", "vihaan@gmail.com", "9876543212"),
    ("Ananya Gupta", "ananya@gmail.com", "9876543213"),
    ("Arjun Reddy", "arjun@gmail.com", "9876543214"),
    ("Diya Mehta", "diya@gmail.com", "9876543215"),
    ("Reyansh Kumar", "reyansh@gmail.com", "9876543216"),
    ("Saanvi Desai", "saanvi@gmail.com", "9876543217"),
    ("Aryan Joshi", "aryan@gmail.com", "9876543218"),
    ("Myra Shah", "myra@gmail.com", "9876543219"),
]

for name, email, mobile in patients:
    first, last = name.split(" ", 1)
    CustomUser.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first,
            'last_name': last,
            'role': 'patient',
            'mobile_number': mobile,
            'password': make_password('patient123'),
        }
    )

# 6. Create Lab Tests (Categories + Tests)
cat, _ = LabTestCategory.objects.get_or_create(name="Blood Tests")
LabTest.objects.bulk_create([
    LabTest(category=cat, name="CBC", price=350, fasting_required=False),
    LabTest(category=cat, name="Blood Sugar Fasting", price=120, fasting_required=True),
    LabTest(category=cat, name="Lipid Profile", price=650, fasting_required=True),
    LabTest(category=cat, name="Thyroid Profile", price=850, fasting_required=False),
    LabTest(category=cat, name="Vitamin D", price=1400, fasting_required=False),
])

# 7. Create Sample Appointments & Reviews
doctors = Doctor.objects.all()
patients = CustomUser.objects.filter(role='patient')[:8]
slots = Slot.objects.all()

for i, doctor in enumerate(doctors[:6]):
    for j in range(3):
        appt_date = date.today() - timedelta(days=30 - i*5 - j)
        appointment = Appointment.objects.create(
            patientid=patients[i % 8],
            doctorid=doctor,
            slotid=slots[j % 6],
            date=appt_date,
            status='completed',
            symptoms="Fever, headache, body pain"
        )
        
        # Add review
        DoctorReview.objects.create(
            doctor=doctor,
            patient=patients[i % 8],
            appointment=appointment,
            rating=5 if j == 0 else 4,
            comment="Excellent doctor! Very caring and knowledgeable."
        )

print("DEMO DATA CREATED SUCCESSFULLY!")
print("\nLogin Details:")
print("Admin   → admin@healthplus.com / admin123")
print("Doctor  → dr.rajesh.sharma@healthplus.com / doctor123")
print("Patient → aarav@gmail.com / patient123")
print("\nGo to http://127.0.0.1:8000 and explore!")