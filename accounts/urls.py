from accounts.views import create_staff, userLogin, userLogout, staff_list, edit_staff, delete_staff
from django.urls import path

urlpatterns = [
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),
    path('staff/', staff_list, name='staff_list'),
    path('staff/create/', create_staff, name='create_staff'),
    path('staff/<int:staff_id>/edit/', edit_staff, name='edit_staff'),
    path('staff/<int:staff_id>/delete/', delete_staff, name='delete_staff'),
]
