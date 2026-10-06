from django.urls import path
from .views import bookAppointment

urlpatterns = [
    path('book/', bookAppointment, name='book_appointment'),
]