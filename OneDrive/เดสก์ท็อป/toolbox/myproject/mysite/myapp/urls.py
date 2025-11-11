# ...existing code...
from django.urls import path
from . import views

urlpatterns = [
 path ('', views.home, name='home'),  # หน้า landing ของคุณ
   
] 