from django.contrib.auth import authenticate, login, logout as lout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from healthcare.models import CustomUser

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Basic validation
        if not email or not password:
            messages.error(request, "Please fill in both email and password.")
            return redirect('signin')

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        # Note: If you're using email as username, make sure your CustomUser uses EMAIL_FIELD = 'email'

        if user is not None:
            if user.is_active:
                login(request, user)

                # Optional: Redirect doctors to their dashboard
                if user.role == "doctor": # Adjust based on your model
                    return redirect("doctors/doctor")  # Your doctor panel URL
                elif user.is_superuser and user.role == "admin":
                    return redirect('admin')
                else:
                    messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                    return redirect('home')  # Regular patient goes to home

            else:
                messages.error(request, "Your account is disabled. Contact support.")
        else:
            messages.error(request, "Invalid email or password. Please try again.")

        return redirect('signin')  # Always redirect after POST

    else:
        # GET request → show login page
        if request.user.is_authenticated:
            return redirect('home')  # Already logged in → go home

        return render(request, 'auth/login.html')  # Your beautiful login page

def register(request):
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip().lower()
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            mobile_number = request.POST.get('mobile_number', '').strip()
            address = request.POST.get('address', '').strip()
            profile_image = request.FILES.get('profile_image')  # Use FILES, not POST!

            # === Validation ===
            if not all([first_name, last_name, email, password1, mobile_number, address]):
                messages.error(request, "All fields are required.")
                return redirect('register')

            if password1 != password2:
                messages.error(request, "Passwords do not match!")
                return redirect('register')

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered.")
                return redirect('register')

            if len(mobile_number) != 10 or not mobile_number.isdigit():
                messages.error(request, "Enter a valid 10-digit mobile number.")
                return redirect('register')

            # === Create User ===
            user = CustomUser.objects.create_user(
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                mobile_number=mobile_number,
                address=address
            )

            # Handle profile image
            if profile_image:
                # Optional: Validate image size (< 2MB)
                if profile_image.size > 2 * 1024 * 1024:
                    messages.error(request, "Image size should be less than 2MB.")
                    user.delete()
                    return redirect('register')
                user.image = profile_image

            user.save()

            # Optional: Auto-login after register
            login(request, user)

            messages.success(request, f"Welcome {first_name}! Your account has been created successfully.")
            return redirect('home')  # or patient dashboard

        except Exception as e:
            messages.error(request, "Registration failed. Please try again.")
            print(f"Registration error: {e}")  # For debugging
            return redirect('register')

    else:
        # GET request
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'auth/register.html')

login_required(login_url='login')
def logout(request):
    lout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('signin')