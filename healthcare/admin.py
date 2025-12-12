from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    CustomUser, Doctor, Speciality, Slot,
    DoctorWeeklySchedule, DoctorSchedule, DoctorLeave,
    Appointment, Prescription, Payment, Notification, Feedback, ContactUs
)

# ===================================================================
# 1. Custom User Admin
# ===================================================================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'mobile_number', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'mobile_number')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'mobile_number', 'gender', 'dob', 'address', 'image')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'role', 'first_name', 'last_name')
        }),
    )


# ===================================================================
# 2. Speciality
# ===================================================================
@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor_count')
    search_fields = ('name',)

    def doctor_count(self, obj):
        count = obj.doctors.count()
        url = reverse("admin:healthcare_doctor_changelist") + f"?speciality__id__exact={obj.id}"
        return format_html('<a href="{}">{} Doctors</a>', url, count)
    doctor_count.short_description = "Doctors"


# ===================================================================
# 3. Doctor Admin (Best One)
# ===================================================================
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'speciality', 'fees', 'experience_years', 'rating', 'is_verified', 'total_appointments','verification_action')
    list_filter = ('is_verified', 'speciality', 'fees')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'degree')
    readonly_fields = ('rating', 'total_reviews')

    fieldsets = (
        ('Doctor Info', {'fields': ('user', 'speciality', 'degree', 'experience_years', 'fees', 'consultation_time')}),
        ('Status', {'fields': ('is_verified', 'rating', 'total_reviews')}),
    )

    def user_link(self, obj):
        url = reverse("admin:healthcare_customuser_change", args=[obj.user.id])
        return format_html('<a href="{}"><strong>Dr. {}</strong></a>', url, obj.user.get_full_name())
    user_link.short_description = "Doctor"

    def total_appointments(self, obj):
        count = obj.appointments.count()
        return format_html('<b>{}</b>', count)
    total_appointments.short_description = "Total Appts"

    def verification_action(self, obj):
        if not obj.is_verified:
            url = reverse('admin:healthcare_doctor_change', args=[obj.id])
            return format_html('<a class="btn btn-success btn-sm" href="{}">Verify Now</a>', url)
        return format_html('<span class="text-success">Verified</span>')
    verification_action.short_description = "Action"


# ===================================================================
# 4. Time Slots
# ===================================================================
@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('slot_time', 'start_time', 'end_time')
    ordering = ('start_time',)


# ===================================================================
# 5. Doctor Weekly & Daily Schedule
# ===================================================================
@admin.register(DoctorWeeklySchedule)
class DoctorWeeklyScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'get_day', 'slot')
    list_filter = ('day_of_week', 'doctor__user__first_name')
    search_fields = ('doctor__user__email',)

    def get_day(self, obj):
        return obj.get_day_of_week_display()
    get_day.short_description = "Day"


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctorid', 'date', 'slotid', 'status_colored', 'booked_by')
    list_filter = ('date', 'status', 'doctorid__user__first_name')
    date_hierarchy = 'date'
    search_fields = ('doctor__user__email',)

    def status_colored(self, obj):
        color = "green" if obj.status else "red"
        text = "Available" if obj.status else "Booked/Leave"
        return format_html('<span style="color:{}"><b>{}</b></span>', color, text)
    status_colored.short_description = "Status"

    def booked_by(self, obj):
        try:
            appt = Appointment.objects.get(doctorid=obj.doctorid, slotid=obj.slotid, date=obj.date)
            return appt.patientid.get_full_name()
        except Appointment.DoesNotExist:
            return "—"
    booked_by.short_description = "Patient"


# ===================================================================
# 6. Leave Management
# ===================================================================
@admin.register(DoctorLeave)
class DoctorLeaveAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start_date', 'end_date', 'reason', 'created_at')
    list_filter = ('start_date', 'doctor__user__first_name')
    date_hierarchy = 'start_date'


# ===================================================================
# 7. Appointments
# ===================================================================
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'doctor_name', 'date', 'slotid', 'status', 'created_at')
    list_filter = ('status', 'date', 'doctorid__user__first_name')
    search_fields = ('patientid__email', 'patientid__first_name')
    date_hierarchy = 'date'

    def patient_name(self, obj):
        return obj.patientid.get_full_name() or obj.patientid.email
    def doctor_name(self, obj):
        return f"Dr. {obj.doctorid}"
    patient_name.short_description = "Patient"
    doctor_name.short_description = "Doctor"


# ===================================================================
# 8. Prescription
# ===================================================================
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'prescribed_by', 'date_issued', 'follow_up_date', 'is_sent')
    list_filter = ('date_issued', 'is_sent')
    search_fields = ('appointment__patientid__email',)


# ===================================================================
# 9. Payment
# ===================================================================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount', 'is_paid', 'paid_at')
    list_filter = ('is_paid', 'paid_at')
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id')


# ===================================================================
# 10. Others
# ===================================================================
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'replied', 'created_at')
    list_filter = ('replied', 'created_at')
    actions = ['mark_as_replied']

    def mark_as_replied(self, request, queryset):
        queryset.update(replied=True)
    mark_as_replied.short_description = "Mark selected as replied"


# ===================================================================
# Nice Admin Header
# ===================================================================
admin.site.site_header = "HealthPlus Admin"
admin.site.site_title = "HealthPlus Admin"
admin.site.index_title = "Welcome to HealthPlus Management"