from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

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