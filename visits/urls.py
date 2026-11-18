from django.urls import path
from . import views

app_name = 'visits'

urlpatterns = [
    path('patient/<int:patient_pk>/history/', views.patient_history_view, name='patient_history'),
    path('patient/<int:patient_pk>/visit/add/', views.add_visit_notes_view, name='add_visit_notes'),
    path('visit/<int:visit_pk>/notes/edit/', views.edit_visit_notes_view, name='edit_visit_notes'),
    path('visit/<int:visit_pk>/complete/', views.complete_visit_view, name='complete_visit'),
    path('billing/', views.admin_billing_dashboard, name='admin_billing'),
    path('billing/generate/<int:invoice_pk>/', views.generate_invoice_view, name='generate_invoice'),
]