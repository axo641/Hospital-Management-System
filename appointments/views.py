from django.shortcuts import render, redirect
from .forms import AppointmentForm

def bookAppointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_appointment')  # Redirect to a success page
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointment.html', {'form': form})

# Create your views here.
