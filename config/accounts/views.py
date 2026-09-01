from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def login_view(request):


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        authenticate_user = authenticate(request, username=username, password=password)

        if authenticate_user is not None:
            login(request, authenticate_user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def home_view(request):
    return render(request, 'home.html')

# Create your views here.
