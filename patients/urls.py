from django.urls import path
from .views import search_patients, register_patient

urlpatterns = [
    path('search/', search_patients, name='patient_search'),
    path('register/', register_patient, name='register_patient'),
]