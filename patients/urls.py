from django.urls import path
from .views import search_patients

urlpatterns = [
    path('search/', search_patients, name='patient_search'),
]