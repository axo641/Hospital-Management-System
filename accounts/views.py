from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
form .forms import CustomUserCreationForm, StaffCreationForm

# Create your views here.

# SO-1: Build backend logic for the user to login
def userLogin(request):
    # Determine whether user is submitting data via POST or GET request
    if request.method == 'POST':
        
        # Handle the login using Django's built-in AuthenticationForm for POST submissions
        form = AuthenticationForm(request, data=request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Extract the username and password from the form data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Check if the user exists and the credentials are correct
            user = authenticate(request, username=username, password=password)

            # If the user is authenticated, log them in and redirect to the home page
            if user is not None:
                login(request, user)
                return redirect('home')

            # If the user is not authenticated, return an 'invalid login' error message
            else:
                return render(request, 'accounts/login.html', 
                              {'form': form, 'error': 'Invalid username or password.'})
        
        # If the form is not valid, return an 'invalid login' error message
        else:
            return render(request, 'accounts/login.html', 
                          {'form': form, 'error': 'Invalid username or password.'})
    
    # If the request method is GET, render the login form
    else:
        form = AuthenticationForm()
    
    # Render the login page with the form
    return render(request, 'accounts/login.html', {'form': form})

# SO-4: Set-up user accounts database where current users reside and new 
# users can be added
def register(request):
    # Determine whether user is submitting data via POST or GET request
    if request.method == 'POST':

        # Handle the registration using the CustomUserCreationForm for POST submissions
        form = CustomUserCreationForm(request.POST)

        # Check if the form is valid
        if form.is_valid():

            # Save the new user to the database
            user = form.save()

            # Log the user in and redirect to the home page
            login(request, user)
            return redirect('home')
    else:
        # If the request method is GET, render the registration form
        form = CustomUserCreationForm()

    # Render the registration page with the form
    return render(request, 'accounts/register.html', {'form': form})

def createStaff(request):
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_staff')  # Redirect to login page after successful registration
    else:
        form = StaffCreationForm()
    return render(request, 'accounts/create_staff.html', {'form': form})

