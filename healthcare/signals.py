from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DoctorLeave, DoctorSchedule
from datetime import timedelta

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