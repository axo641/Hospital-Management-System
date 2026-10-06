from accounts.views import createStaff, userLogin
from django.urls import path

urlpatterns = [
    path('login/', userLogin, name='login'),
    path('create/', createStaff, name='create_staff')
]