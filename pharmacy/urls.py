from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('prescriptions/', views.prescription_list_view, name='pharmacist_prescriptions'),
    path('prescriptions/add/', views.prescription_create_view, name='prescription_add'),
    path('prescriptions/<int:pk>/', views.prescription_detail_view, name='prescription_detail'),
    path('prescriptions/<int:pk>/print/', views.print_prescription_view, name='print_prescription'),
    path('visit/<int:visit_pk>/prescribe/', views.prescribe_for_visit_view, name='prescribe_for_visit'),
    path('my-prescriptions/', views.patient_prescriptions_view, name='patient_prescriptions'),
]