from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('Admin/<int:user_id>/', views.Admin_view, name='Admin'),
    path('Employee/<int:user_id>', views.Employee_view, name='Employee'),
    path('Manager/<int:user_id>', views.Manager_view, name='Manager'),
    path('admin_action/<int:user_id>/<int:request_id>/', views.admin_action, name='admin_action'),
    path('create_course/<int:user_id>/', views.create_course, name='create_course'),
    path('view_course/<int:course_id>/<int:user_id>/', views.view_course, name='view_course'),
    path('feedback_form/<int:course_id>/<int:user_id>/',views.feedback_view,name='feedback_form'),
    path('feedback_tracker/<int:user_id>/',views.feedback_tracker,name='feedback_tracker'),
    path('general_feedback/<int:user_id>/',views.general_feedback_view, name='general_feedback'),
    path('progress/', views.progress_view, name='employee_progress'),

    path('notifications/<int:user_id>/', views.notifications_view, name='notifications'),  # User-specific notifications
    path('notifications/mark-all-as-read/<int:user_id>/', views.mark_all_as_read, name='mark_all_as_read'),  # Mark all as read

    

]
