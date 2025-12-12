# healthcare/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    CustomUser, Doctor, Speciality, Slot,
    DoctorWeeklySchedule, DoctorSchedule, DoctorLeave,
    Appointment, Prescription,
    ChatRoom, ChatMessage,
    LabTestCategory, LabTest, LabBooking,
    Feedback, ContactUs
)

# =========================================
# 1. Custom User Admin
# =========================================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'mobile_number', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'mobile_number')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'mobile_number', 'gender', 'dob', 'address', 'image')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role')
        }),
    )


# =========================================
# 2. Doctor Admin (with Verify Button)
# =========================================
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'speciality', 'fees', 'is_verified', 'rating', 'verify_button')
    list_filter = ('is_verified', 'speciality')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('rating', 'total_reviews')

    def user_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.email
    user_full_name.short_description = "Doctor"

    def verify_button(self, obj):
        if not obj.is_verified:
            url = reverse('admin:healthcare_doctor_changelist')
            return format_html(
                '<a class="button" href="{}?is_verified=False">Verify All Pending</a> | '
                '<a class="button btn-success" href="{}">Verify Now</a>',
                url,
                reverse('admin:healthcare_doctor_change', args=[obj.pk])
            )
        return format_html('<span class="text-success">Verified</span>')
    verify_button.short_description = "Action"
    verify_button.allow_tags = True


# =========================================
# 3. Lab Tests Admin (Full Control)
# =========================================
@admin.register(LabTestCategory)
class LabTestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'tests_count', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

    def tests_count(self, obj):
        return obj.tests.count()
    tests_count.short_description = "Tests"


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'fasting_required', 'turnaround_time')
    list_filter = ('category', 'fasting_required')
    search_fields = ('name', 'category__name')


@admin.register(LabBooking)
class LabBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'tests_list', 'appointment_date', 'appointment_time', 'status', 'total_amount')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient__email', 'patient__first_name')
    readonly_fields = ('total_amount', 'created_at')

    def patient_name(self, obj):
        return obj.patient.get_full_name()
    patient_name.short_description = "Patient"

    def tests_list(self, obj):
        return ", ".join([t.name for t in obj.tests.all()[:3]]) + ("..." if obj.tests.count() > 3 else "")
    tests_list.short_description = "Tests"


# =========================================
# 4. Appointments & Prescriptions
# =========================================
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'doctor_name', 'date', 'slotid', 'status')
    list_filter = ('status', 'date', 'doctorid__speciality')
    search_fields = ('patientid__email', 'doctorid__user__email')

    def patient_name(self, obj): return obj.patientid.get_full_name()
    def doctor_name(self, obj): return f"Dr. {obj.doctorid.user.get_full_name()}"


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'doctor_name', 'date_issued', 'follow_up_date')
    list_filter = ('date_issued',)
    search_fields = ('appointment__patientid__email',)

    def patient_name(self, obj): return obj.appointment.patientid.get_full_name()
    def doctor_name(self, obj): return f"Dr. {obj.prescribed_by.user.get_full_name()}"


# =========================================
# 5. Chat System Admin
# =========================================
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('patient__email', 'doctor__user__email')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('chat_room', 'sender_name', 'message_preview', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender__email', 'message')

    def sender_name(self, obj): return obj.sender.get_full_name()
    def message_preview(self, obj): return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message


# =========================================
# 6. Feedback & Contact
# =========================================
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('user', 'rating', 'message', 'created_at')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'replied', 'created_at')
    list_filter = ('replied', 'created_at')
    actions = ['mark_as_replied']

    def mark_as_replied(self, request, queryset):
        queryset.update(replied=True)
    mark_as_replied.short_description = "Mark as replied"


# =========================================
# 7. Other Models
# =========================================
@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor_count')
    search_fields = ('name',)

    def doctor_count(self, obj):
        return obj.doctors.count()


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('slot_time', 'start_time', 'end_time')
    ordering = ('start_time',)


# Nice Admin Header
admin.site.site_header = "HealthPlus Hospital - Admin Panel"
admin.site.site_title = "HealthPlus Admin"
admin.site.index_title = "Welcome to HealthPlus Management"