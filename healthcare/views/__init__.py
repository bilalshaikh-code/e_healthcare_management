from .auth import *
from .index import *
from .dashboard import patient_dashboard
from .profile import patient_profile
from .booking import book_appointment, get_available_slots, confirm_booking
from .appointments import my_appointments, cancel_appointment, appointment_history
from .prescription import my_prescriptions, prescription_detail, download_prescription_pdf
from .chat import patient_chat_list
from .lab import lab_test_booking, lab_booking_success
from .rating import rate_doctor