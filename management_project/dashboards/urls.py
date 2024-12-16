from django.urls import path
from . import views

urlpatterns = [
    
    path('Admin/', views.Admin_view, name='Admin'),
    path('Employee/', views.Employee_view, name='Employee'),
    path('Manager/', views.Manager_view, name='Manager'),
]