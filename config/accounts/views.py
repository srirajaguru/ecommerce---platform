import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import RegisterForm
from .models import CustomUser


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.is_email_verified = False

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
        {'form': form}
    )

def send_otp(user, request):

    otp = str(random.randint(100000, 999999))

    request.session['registration_otp'] = otp
    request.session['registration_username'] = user.username

    send_mail(
        subject='Sri Annai Precast - Email Verification OTP',

        message=f"""
Hello {user.name},

Your email verification OTP is:

{otp}

Please enter this OTP to verify your email address.

Thank you,
Sri Annai Precast
""",

        from_email=settings.DEFAULT_FROM_EMAIL,

        recipient_list=[user.email],

        fail_silently=False,
    )


def verify_otp_view(request):

    if request.method == 'POST':

        entered_otp = request.POST.get('otp')

        saved_otp = request.session.get('registration_otp')

        username = request.session.get('registration_username')

        if not saved_otp or not username:

            messages.error(
                request,
                'OTP session expired. Please register again.'
            )

            return redirect('register')

        if entered_otp == saved_otp:

            try:

                user = CustomUser.objects.get(
                    username=username
                )

                user.is_email_verified = True

                user.save()

                # Remove OTP from session
                request.session.pop(
                    'registration_otp',
                    None
                )

                request.session.pop(
                    'registration_username',
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
                'Invalid OTP.'
            )

    return render(
        request,
        'verify_otp.html'
    )

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.is_email_verified:

                messages.error(
                    request,
                    'Please verify your email before logging in.'
                )

                return redirect('login')

            if not user.is_active:

                messages.error(
                    request,
                    'Your account is inactive.'
                )

                return redirect('login')

            login(request, user)

            messages.success(
                request,
                f'Welcome back, {user.name}!'
            )

            return redirect('home')

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(
        request,
        'login.html'
    )

def logout_view(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect('login')

