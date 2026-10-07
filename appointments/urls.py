from django.urls import path
from .views import appointment_list, create_appointment, edit_appointment, delete_appointment

urlpatterns = [
    path('', appointment_list, name='appointment_list'),
    path('create/', create_appointment, name='create_appointment'),
    path('<int:appointment_id>/edit/', edit_appointment, name='edit_appointment'),
    path('<int:appointment_id>/delete/', delete_appointment, name='delete_appointment'),
]
