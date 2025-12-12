# HealthPlus Hospital Management System

A **full-stack, production-ready hospital management system** built with Django — just like Practo, Apollo 24|7, and Lybrate.

Patients can book appointments, view prescriptions, and manage their health.  
Doctors get a powerful dashboard, calendar, weekly scheduling, leave system, and prescription tools.  
Admins have full control via Django Admin.

**Live in minutes. No paid tools needed.**

[![Django](https://img.shields.io/badge/Django-5.0-brightgreen)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5.3-purple)](https://getbootstrap.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

| For Patients                        | For Doctors                          | For Admin                          |
|------------------------------------|---------------------------------------|------------------------------------|
| Register & Login                   | Weekly auto-scheduling                | Full Django Admin Panel            |
| Book appointment (live slots)      | FullCalendar view (FullCalendar.js)     | Approve/reject doctors             |
| View upcoming & past appointments   | Take leave / block dates              | View all appointments & payments   |
| View & download PDF prescriptions   | Send digital prescriptions             | Manage specialities & time slots   |
| Edit profile + photo               | View patient history                 | Export data                        |
| Responsive mobile design            | Notification bell                      |                                     |

---

## Tech Stack

- **Backend**: Django 5.0 + PostgreSQL (or SQLite for dev)
- **Frontend**: Bootstrap 5, Font Awesome, FullCalendar.js
- **PDF Generation**: WeasyPrint** (beautiful prescriptions)
- **Authentication**: Email-based login (no username)
- **Deployment-ready**: Works on Railway, Render, PythonAnywhere, Heroku

---

## Quick Start (5 minutes)

```bash
git clone https://github.com/yourname/healthplus-hospital.git
cd healthplus-hospital

# Create virtual env
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (for admin)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Visit:-

- [http://127.0.0.1:8000] -> Home
- [http://127.0.0.1:8000/admin] -> Admin Panel
- Register as Patient or Doctor

---

### Default Roles

| Email                    | Password | Role   | Access After Login            |
|--------------------------|----------|--------|------------------------------|
| [admin@healthplus.com](mailto:admin@healthplus.com)      | admin123 | Admin  | `/admin/`                    |
| [doctor@healthplus.com](mailto:doctor@healthplus.com)     | doctor123| Doctor | `/doctor/` (after approval)   |
| [patient@healthplus.com](mailto:patient@healthplus.com)    | patient123| Patient| `/patient/dashboard/`          |

> New doctors need admin approval from `/admin/`

---

### Project Structure

```text
healthplus/
├── healthcare/              # Main app
│   ├── models.py           # All models (User, Doctor, Appointment, Prescription++)
│   ├── views/
│   │   ├── patient.py      # Patient views
│   │   └── doctor.py       # Doctor views
│   ├── templates/
│   │   ├── patient/        # Patient portal
│   │   └── doctor/         # Doctor portal
│   └── admin.py            # Beautiful admin panel
├── static/
│   └── css/                # Custom styles
├── requirements.txt
└── manage.py
```

---

### Screenshots

| Patient Dashboard | Doctor Calendar | Prescription PDF |
|------------------|----------------|------------------|
| ![Patient Dashboard] | ![Doctor Calendar] | ![Prescription] |

- *(Add your own screenshots later!)*

---

### Deployment (One-Click)

Deploy free on:-

- [Railway.app](https://railway.app) → Just connect GitHub
- [Render.com](https://render.com)
- PythonAnywhere (free tier works)

I can give you the exact deploy steps in 2 minutes — just say **DEPLOY**

---

### Made with ❤️ by You

**HealthPlus** is 100% open source and free forever.

Want to add:-

- SMS alerts (Twilio)
- Online payment (Razorpay/Stripe)
- Video consultation
- Mobile app (React Native)

Just ask — I’ll build it for you!

**Star this repo if you love it!**
[![Star](https://img.shields.io/github/stars/yourname/healthplus-hospital?style=social)](https://github.com/yourname/healthplus-hospital)
