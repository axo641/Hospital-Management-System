from django.urls import path
from .views import (
    appointment_list, 
    create_appointment, 
    edit_appointment, 
    delete_appointment, 
    doctor_schedule, 
    check_patient_in,
    patient_appointments_dashboard,        
    request_appointment_cancellation,
    generate_reports,    
)

urlpatterns = [
    path('', appointment_list, name='appointment_list'),
    path('create/', create_appointment, name='create_appointment'),
    path('<int:appointment_id>/edit/', edit_appointment, name='edit_appointment'),
    path('<int:appointment_id>/delete/', delete_appointment, name='delete_appointment'),
    path('<int:appointmentID>/check-in/', check_patient_in, name='check_patient_in'),
    path('schedule/', doctor_schedule, name='doctor_schedule'),
    path('my-appointments/', patient_appointments_dashboard, name='patient_appointments_dashboard'),
    path('my-appointments/<int:appointment_id>/request-cancel/', request_appointment_cancellation, name='request_appointment_cancellation'),
    path('reports/', generate_reports, name='generate_reports'),
]
