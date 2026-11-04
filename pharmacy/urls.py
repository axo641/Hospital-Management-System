from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('prescriptions/', views.prescription_list_view, name='pharmacist_prescriptions'),
    path('prescriptions/add/', views.prescription_create_view, name='prescription_add'),
    path('prescriptions/<int:pk>/', views.prescription_detail_view, name='prescription_detail'),
    path('my-prescriptions/', views.patient_prescriptions_view, name='patient_prescriptions'),
]
