import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone

from .forms import RegisterForm
from .models import CustomUser


# =========================================================
# REGISTER
# =========================================================

def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # Customer must verify email
            user.is_email_verified = False

            # Make sure normal customer is not staff
            user.is_staff = False
            user.is_superuser = False

            user.save()

            # Send OTP
            send_otp(user, request)

            messages.success(
                request,
                'Registration successful. OTP has been sent to your email.'
            )

            return redirect('verify_otp')

    else:

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


# =========================================================
# SEND OTP
# =========================================================

def send_otp(user, request):

    # Generate 6 digit OTP
    otp = str(random.randint(100000, 999999))

    # OTP expiry time
    otp_created_at = timezone.now()

    # Store OTP in session
    request.session['registration_otp'] = otp
    request.session['registration_username'] = user.username
    request.session['otp_created_at'] = otp_created_at.isoformat()

    # Send email
    send_mail(

        subject='Sri Annai Precast - Email Verification OTP',

        message=f"""
Hello {user.name},

Thank you for registering with Sri Annai Precast.

Your email verification OTP is:

{otp}

This OTP is valid for 5 minutes.

Please do not share this OTP with anyone.

Thank you,
Sri Annai Precast
""",

        from_email=settings.DEFAULT_FROM_EMAIL,

        recipient_list=[
            user.email
        ],

        fail_silently=False,
    )


# =========================================================
# VERIFY OTP
# =========================================================

def verify_otp_view(request):

    # Check whether registration session exists
    username = request.session.get(
        'registration_username'
    )

    if not username:

        messages.error(
            request,
            'OTP session expired. Please register again.'
        )

        return redirect('register')

    if request.method == 'POST':

        entered_otp = request.POST.get(
            'otp'
        )

        saved_otp = request.session.get(
            'registration_otp'
        )

        otp_created_at = request.session.get(
            'otp_created_at'
        )

        # Check OTP exists
        if not saved_otp or not otp_created_at:

            messages.error(
                request,
                'OTP expired. Please request a new OTP.'
            )

            return redirect('verify_otp')

        # Convert stored time back to datetime
        try:

            otp_created_time = timezone.datetime.fromisoformat(
                otp_created_at
            )

        except ValueError:

            messages.error(
                request,
                'Invalid OTP session. Please register again.'
            )

            return redirect('register')

        # Make timezone aware if required
        if timezone.is_naive(otp_created_time):

            otp_created_time = timezone.make_aware(
                otp_created_time
            )

        # Check 5 minute expiry
        if timezone.now() > otp_created_time + timedelta(minutes=5):

            # Remove expired OTP
            request.session.pop(
                'registration_otp',
                None
            )

            request.session.pop(
                'otp_created_at',
                None
            )

            messages.error(
                request,
                'OTP has expired. Please request a new OTP.'
            )

            return redirect('verify_otp')

        # Check OTP
        if entered_otp == saved_otp:

            try:

                user = CustomUser.objects.get(
                    username=username
                )

                # Verify email
                user.is_email_verified = True

                user.save(
                    update_fields=[
                        'is_email_verified'
                    ]
                )

                # Remove OTP session
                request.session.pop(
                    'registration_otp',
                    None
                )

                request.session.pop(
                    'registration_username',
                    None
                )

                request.session.pop(
                    'otp_created_at',
                    None
                )

                messages.success(
                    request,
                    'Email verified successfully. You can now login.'
                )

                return redirect('login')

            except CustomUser.DoesNotExist:

                messages.error(
                    request,
                    'User not found.'
                )

                return redirect('register')

        else:

            messages.error(
                request,
                'Invalid OTP. Please try again.'
            )

    return render(
        request,
        'verify_otp.html'
    )


# =========================================================
# RESEND OTP
# =========================================================

def resend_otp_view(request):

    username = request.session.get(
        'registration_username'
    )

    if not username:

        messages.error(
            request,
            'Registration session expired. Please register again.'
        )

        return redirect('register')

    try:

        user = CustomUser.objects.get(
            username=username
        )

        # Don't resend if already verified
        if user.is_email_verified:

            messages.info(
                request,
                'Your email is already verified.'
            )

            return redirect('login')

        # Generate and send new OTP
        send_otp(
            user,
            request
        )

        messages.success(
            request,
            'A new OTP has been sent to your email.'
        )

        return redirect('verify_otp')

    except CustomUser.DoesNotExist:

        messages.error(
            request,
            'User not found.'
        )

        return redirect('register')


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        # Authenticate username/password
        user = authenticate(
            request,
            username=username,
            password=password
        )

        # =================================================
        # INVALID LOGIN
        # =================================================

        if user is None:

            messages.error(
                request,
                'Invalid username or password.'
            )

            return redirect('login')

        # =================================================
        # ACCOUNT INACTIVE
        # =================================================

        if not user.is_active:

            messages.error(
                request,
                'Your account is inactive.'
            )

            return redirect('login')

        # =================================================
        # ADMIN LOGIN
        # =================================================

        if user.is_staff:

            login(
                request,
                user
            )

            messages.success(
                request,
                f'Welcome Admin, {user.name or user.username}!'
            )

            return redirect('dashboard')

        # =================================================
        # CUSTOMER LOGIN
        # =================================================

        if not user.is_email_verified:

            messages.error(
                request,
                'Please verify your email before logging in.'
            )

            # Save username so user can request OTP
            request.session[
                'registration_username'
            ] = user.username

            return redirect('login')

        # =================================================
        # CUSTOMER SUCCESSFUL LOGIN
        # =================================================

        login(
            request,
            user
        )

        messages.success(
            request,
            f'Welcome back, {user.name}!'
        )

        return redirect('home')

    return render(
        request,
        'login.html'
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect('login')