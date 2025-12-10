from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manage import UserManager

# ============================
# User Models
# ============================

class CustomUser(AbstractUser):
    """
    Custom user model using email as login.
    Roles:
        - Admin
        - Patient
        - Doctor
    """
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("patient", "Patient"),
        ("doctor", "Doctor"),
    )

    username = None
    email = models.EmailField(unique=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="patient")

    mobile_number = models.CharField(max_length=14, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='pics/users', null=True, blank=True)

    reset_token = models.CharField(max_length=100, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

# ============================
# Doctor Models
# ============================

class Speciality(models.Model):
    """
    Represents a medical specialty for doctors (e.g., Cardiology, Dermatology, Neurology, etc.).
    Each specialty has a name and an optional description to provide more details.
    """
    name = models.CharField(
        max_length=50,  # Increased length for longer specialty names
        unique=True,
        help_text="Name of the medical specialty (e.g., Cardiology)"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description of the specialty."
    )

    class Meta:
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"
        ordering = ['name']  # Orders specialties alphabetically

    def __str__(self):
        return self.name

class Doctor(models.Model):
    """
    Doctor profile — contains only doctor-specific data.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=15, null=True, blank=True)

    degree = models.CharField(max_length=50)
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)
    fees = models.IntegerField()

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# ============================
# Appointment & Schedule Models
# ============================

class Slot(models.Model):
    """
    Represents a time slot for appointments.
    """
    time = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.time}"

class Appointment(models.Model):
    """
    Appointment between patient and doctor at a specific slot.
    """
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=50)  # e.g., booked, completed, canceled

    def __str__(self):
        return f"Appointment: {self.patient} with {self.doctor} on {self.date}"

class DoctorWeeklySchedule(models.Model):
    """
    Doctor sets his weekly template once → system auto-creates daily slots
    Example: Dr. Tirth works every Mon, Wed, Fri from 10 AM - 1 PM & 4 PM - 7 PM
    """
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='weekly_schedule')
    day_of_week = models.CharField(max_length=10, choices=[
        ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')
    ])
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'day_of_week', 'slot')
        ordering = ['day_of_week', 'slot']

    def __str__(self):
        return f"{self.doctor} → {self.get_day_of_week_display()} {self.slot}"
    
    def get_day_of_week_display(self):
        return f"{self.day_of_week}"

# ============================
# Payment Models
# ============================

class Payment(models.Model):
    """
    Payment records for appointments via RazorPay.
    """
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    fees = models.IntegerField()
    status = models.BooleanField(default=False)
    razorpay_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_pay_signature_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Payment for {self.appointment}"

# ============================
# Chat / Communication Models
# ============================

class Chatbot(models.Model):
    """
    Chat messages between doctor and patient.
    """
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(auto_now=True)
    message = models.CharField(max_length=1000)
    sender = models.CharField(max_length=200)  # Could be 'doctor' or 'patient'

    def __str__(self):
        return f"Chat on {self.date} by {self.sender}"

# ============================
# Feedback / Complaint / Contact Models
# ============================

# Feedback from patients
class Feedback(models.Model):
    p_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    rate = models.CharField(max_length=50)
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"Feedback from {self.p_name}"

# Complaint from patients
class Complain(models.Model):
    patient_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    complain_message = models.CharField(max_length=200)

    def __str__(self):
        return f"Complain from {self.patient_name}"

# General contact messages (anyone can use)
class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=50)
    msg = models.CharField(max_length=100)

    def __str__(self):
        return f"Contact: {self.subject} by {self.name}"

# ============================
# Other / Optional Models
# ============================

class Destination(models.Model):
    """
    Possibly hospital services/packages.
    """
    img = models.ImageField(upload_to='pics', null=True, blank=True)
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

class ShowAppointment(models.Model):
    """
    Additional info per appointment like prescription or chat logs.
    """
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    date = models.DateField()
    prescription = models.CharField(max_length=1000, null=True, blank=True)
    chat = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"Details for {self.appointment}"
