from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout  # Importing authenticate and renaming login to avoid conflicts

def add_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')  # Use get method to avoid KeyError
        last_name = request.POST.get('lastname')
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        pswd1 = request.POST.get('psw1')  # Password entered first time
        pswd2 = request.POST.get('psw2')  # Password entered second time

        # Ensure passwords match
        if pswd1 == pswd2:
            # Check if the username or email is already taken
            if User.objects.filter(username=user_name).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
            else:
                # Create the user with the hashed password
                user = User.objects.create_user(
                    username=user_name,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=pswd1  # Save only one password (hashed automatically)
                )
                user.save()
                messages.success(request, 'User created successfully.')
                return redirect('login')  # Redirect to login after successful registration
        else:
            messages.error(request, 'Passwords do not match.')
        
        return redirect('register')  # Redirect back to registration page on error
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        
        user = authenticate(username=uname, password=pwd)
        
        if user is not None:
            auth_login(request, user)  # Use the aliased login function
            messages.success(request, 'Logged in successfully!')  # Optional success message
            return redirect('/')  # Redirect to the homepage or dashboard after login
        else:
            messages.error(request, 'Invalid credentials!')  # Use error message for invalid credentials
            return redirect('login')
        
    return render(request, 'login.html')





def user_logout(request):  # Renamed to avoid conflict with any built-in logout
    auth_logout(request)
    return redirect('/')


    