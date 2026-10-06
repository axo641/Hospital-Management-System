from accounts.views import userLogin
from django.urls import path

urlpatterns = [
    path('login/', userLogin, name='login'),
]