from django.shortcuts import render
from .models import TrainingRequest

# Create your views here.
def Admin_view(request):
    return render(request, 'dashboards/Admin.html')
def Employee_view(request):
    return render(request, 'dashboards/Employee.html')
def Manager_view(request):
    # Count the number of requests based on the status
    pending = TrainingRequest.objects.filter(status='Pending').count()
    approved = TrainingRequest.objects.filter(status='Approved').count()
    total = TrainingRequest.objects.count() 
     # Total number of training requests

    context = {
        'total': total,
        'approved': approved,
        'pending': pending,
    }


    return render(request, 'dashboards/Manager.html',context)