# E-Healthcare Management System

A comprehensive healthcare management system built with Django and integrated with RazorPay for payment processing.

## Features

- Patient Management
- Appointment Booking
- Medical Records Management
- Payment Integration with RazorPay
- User Authentication & Authorization
- Medical Staff Management

## Tech Stack

- Backend: Django
- Payment Gateway: RazorPay
- Database: SQLite (default) / PostgreSQL
- Frontend: HTML, CSS, JavaScript

## Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

## Installation

1.Clone the repository:

```bash
git clone [repository-url]
cd e-healthcare-mng
```

2.Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3.Install dependencies:

```bash
pip install -r requirements.txt
```

4.Set up environment variables:

Create a `.env` file in the project root with:

```txt
SECRET_KEY=your_django_secret_key
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

5.Run migrations:

```bash
python manage.py migrate
```

6.Create superuser:

```bash
python manage.py createsuperuser
```

7.Run the development server:

```bash
python manage.py runserver
```

## Configuration

1. RazorPay Integration:
   - Sign up at [https://razorpay.com](Razorpay.com)
   - Get your API keys from the dashboard
   - Add them to your `.env` file

2. Environment Variables:
   - `DEBUG`: Set to True for development, False for production
   - `ALLOWED_HOSTS`: Add your domain name
   - `DATABASE_URL`: For production database configuration

## Security Notes

- Never commit your `.env` file to version control
- Use strong passwords for admin accounts
- Keep your RazorPay API keys secure
- Regularly update dependencies

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
