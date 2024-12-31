from django.urls import path
from . import views

urlpatterns = [
    
    path('Admin/<int:user_id>/', views.Admin_view, name='Admin'),
    path('Employee/<int:user_id>', views.Employee_view, name='Employee'),
    path('Manager/<int:user_id>', views.Manager_view, name='Manager'),
    path('admin_action/<int:user_id>/<int:request_id>/', views.admin_action, name='admin_action'),
    path('create_course/<int:user_id>/', views.create_course, name='create_course'),
    path('view_course/<int:course_id>/<int:user_id>/', views.view_course, name='view_course'),
    path('feedback_form/<int:course_id>/<int:user_id>/',views.feedback_view,name='feedback_form'),
    path('feedback_tracker/<int:user_id>/',views.feedback_tracker,name='feedback_tracker')
]