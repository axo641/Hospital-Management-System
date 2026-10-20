from django.urls import path
from .views import appointment_list, create_appointment, edit_appointment, delete_appointment, doctor_schedule, check_patient_in

urlpatterns = [
    path('', appointment_list, name='appointment_list'),
    path('create/', create_appointment, name='create_appointment'),
    path('<int:appointment_id>/edit/', edit_appointment, name='edit_appointment'),
    path('<int:appointment_id>/delete/', delete_appointment, name='delete_appointment'),
    path('<int:appointmentID>/check-in/', check_patient_in, name='check_patient_in'),
    path('schedule/', doctor_schedule, name='doctor_schedule'),
]
