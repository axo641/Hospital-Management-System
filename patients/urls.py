from django.urls import path
from .views import search_patients, register_patient, medical_records_list, patient_medical_records, add_medical_record, delete_medical_record

urlpatterns = [
    path('search/', search_patients, name='patient_search'),
    path('register/', register_patient, name='register_patient'),
    path('medical-records/', medical_records_list, name='medical_records_list'),
    path('medical-records/<int:patient_id>/', patient_medical_records, name='patient_medical_records'),
    path('medical-records/<int:patient_id>/add/', add_medical_record, name='add_medical_record'),
    path('medical-records/<int:record_id>/delete/', delete_medical_record, name='delete_medical_record'),
]
