from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from healthcare.models import DoctorWeeklySchedule, DoctorSchedule, Slot

class Command(BaseCommand):
    help = 'Auto-create DoctorSchedule rows for next 60 days based on weekly template'

    def handle(self, *args, **options):
        today = timezone.now().date()
        future_date = today + timedelta(days=60)

        for weekly in DoctorWeeklySchedule.objects.filter(is_active=True):
            current = today
            while current <= future_date:
                if current.strftime('%A').lower() == weekly.day_of_week:
                    DoctorSchedule.objects.get_or_create(
                        doctorid=weekly.doctor,
                        slotid=weekly.slot,
                        date=current,
                        defaults={'status': True}
                    )
                current += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS('Successfully generated doctor schedules for next 60 days'))