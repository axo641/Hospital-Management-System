from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    create_staff, userLogin, userLogout,
    staff_list, edit_staff, delete_staff
)

urlpatterns = [
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),
    path('staff/', staff_list, name='staff_list'),
    path('staff/create/', create_staff, name='create_staff'),
    path('staff/<int:staff_id>/edit/', edit_staff, name='edit_staff'),
    path('staff/<int:staff_id>/delete/', delete_staff, name='delete_staff'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
