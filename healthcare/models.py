from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date
from .manage import UserManager
from django.core.validators import MinValueValidator

# ===================================================================
# 1. Custom User (Patient + Doctor + Admin)
# ===================================================================
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )

    username = None
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male','Male'),('female','Female'),('other','Other')], blank=True)
    dob = models.DateField("Date of Birth", null=True, blank=True)
    address = models.TextField(blank=True)
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    @property
    def age(self):
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None


# ===================================================================
# 2. Speciality & Doctor Profile
# ===================================================================
class Speciality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True, related_name='doctors')
    degree = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField(default=0)
    fees = models.PositiveIntegerField(validators=[MinValueValidator(100)])
    consultation_time = models.PositiveSmallIntegerField(default=30, help_text="Minutes per patient")
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

    class Meta:
        ordering = ['user__first_name']


# ===================================================================
# 3. Time Slots
# ===================================================================
class Slot(models.Model):
    slot_time = models.CharField(max_length=50, unique=True)  # "10:00 AM - 10:30 AM"
    start_time = models.TimeField()  # 10:00:00
    end_time = models.TimeField()    # 10:30:00
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.slot_time

    class Meta:
        ordering = ['start_time']


# ===================================================================
# 4. Doctor Weekly Schedule (Set once)
# ===================================================================
class DoctorWeeklySchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='weekly_schedule')
    day_of_week = models.CharField(max_length=10, choices=[
        ('monday','Monday'), ('tuesday','Tuesday'), ('wednesday','Wednesday'),
        ('thursday','Thursday'), ('friday','Friday'), ('saturday','Saturday'), ('sunday','Sunday')
    ])
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'day_of_week', 'slot')


# ===================================================================
# 5. Doctor Daily Availability
# ===================================================================
class DoctorSchedule(models.Model):
    doctorid = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    slotid = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField(db_index=True)
    status = models.BooleanField(default=True)  # True = Available
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctorid', 'slotid', 'date')
        indexes = [models.Index(fields=['date', 'status'])]


# ===================================================================
# 6. Doctor Leave / Holidays
# ===================================================================
class DoctorLeave(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor} → Leave {self.start_date}"


# ===================================================================
# 7. Patient Appointment
# ===================================================================
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )

    patientid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    doctorid = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    slotid = models.ForeignKey(Slot, on_delete=models.CASCADE)
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    symptoms = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('doctorid', 'slotid', 'date')
        ordering = ['-date', 'slotid']


# ===================================================================
# 8. Prescription (Separate & Professional)
# ===================================================================
class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    prescribed_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='prescriptions')
    medicines = models.TextField()
    dosage = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    date_issued = models.DateField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription #{self.id} - {self.appointment.patientid}"


# ===================================================================
# 9. Payment & Notifications
# ===================================================================
class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment')
    amount = models.PositiveIntegerField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


# ===================================================================
# 10. Feedback & Contact
# ===================================================================
class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i,i) for i in range(1,6)])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)