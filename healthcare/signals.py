from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DoctorLeave, DoctorSchedule, DoctorReview
from datetime import timedelta
from django.db.models import Avg
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

@receiver(post_save, sender=DoctorLeave)
def block_leave_dates(sender, instance, created, **kwargs):
    current = instance.start_date
    end = instance.end_date or instance.start_date

    while current <= end:
        DoctorSchedule.objects.filter(
            doctorid=instance.doctor,
            date=current,
            status=True  # Only block if still available
        ).update(status=False)
        current += timedelta(days=1)

@receiver(post_delete, sender=DoctorLeave)
def unblock_leave_dates(sender, instance, **kwargs):
    # Optional: re-activate slots if leave is cancelled
    current = instance.start_date
    end = instance.end_date or instance.start_date
    while current <= end:
        DoctorSchedule.objects.filter(
            doctorid=instance.doctor,
            date=current
        ).update(status=True)
        current += timedelta(days=1)


@receiver([post_save, post_delete], sender=DoctorReview)
def update_doctor_rating(sender, instance, **kwargs):
    doctor = instance.doctor
    reviews = DoctorReview.objects.filter(doctor=doctor)
    count = reviews.count()
    
    if count > 0:
        avg = reviews.aggregate(Avg('rating'))['rating__avg']
        doctor.rating = round(avg, 2)
        doctor.total_reviews = count
    else:
        doctor.rating = 0.00
        doctor.total_reviews = 0
    
    doctor.save(update_fields=['rating', 'total_reviews'])

@receiver(post_save, sender=DoctorSchedule)
def generate_schedule(sender, instance, created, **kwargs):
    if created:
        from doctors.management.commands.generate_doctor_schedules import Command
        cmd = Command()
        cmd.handle()