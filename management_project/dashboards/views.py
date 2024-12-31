from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import TrainingRequest,Course,Module,Notification,Feedback,GeneralFeedback,ModuleCompletion
from authentication.models import User,Role
from .forms import TrainingRequestForm,FeedbackForm,GeneralFeedbackForm,CourseCreationForm,ModuleFormSet
from django.contrib import messages
from django.core.paginator import Paginator

import re

def extract_video_id(url):
        # Regular expression to match YouTube URL formats
        patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',  # For standard YouTube URLs
            r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})'  # For shortened URLs
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)  # Return the video ID

        return None  # Return None if no ID is found

# Create your views here.

def Admin_view(request, user_id):
    admin = get_object_or_404(User, id=user_id)

    if request.method == 'POST' and 'delete_course' in request.POST:
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, course_id=course_id)
        course.delete()
        return redirect('Admin', user_id=user_id)  # Redirect to the admin page after deletion

    context = {
        'admin': admin,
        'user_id': user_id,
        'courses_count': Course.objects.all().count(),
        'pending_count': TrainingRequest.objects.filter(status='Pending').count(),
        'employees_count': User.objects.filter(role=Role.objects.get(role_name='Employee').id).count(),
        'pending_requests': TrainingRequest.objects.filter(status='Pending'),
        'courses': Course.objects.all(),
    }
    return render(request, 'dashboards/Admin.html', context)



def admin_action(request, user_id, request_id):
    task = get_object_or_404(TrainingRequest, request_id=request_id)
    context = {
        'title': task.title,
        'description': task.description,
        'account_manager': task.account_manager
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            task.status = 'Approved'
            task.save()
            return redirect('create_course', user_id=user_id)  # Correct the redirect to pass user_id properly

        elif action == 'reject':
            task.status = 'Rejected'
            task.save()
            return redirect('Admin', user_id=user_id)  # Correct the redirect to pass user_id properly

    return render(request, 'dashboards/admin_action.html', context)



def create_course(request, user_id):
    admin = User.objects.get(id=user_id)  # The user creating the course

    if request.method == 'POST':
        form = CourseCreationForm(request.POST)
        formset = ModuleFormSet(request.POST, request.FILES)  # Handle file uploads

        if form.is_valid() and formset.is_valid():
            course = form.save(commit=False)
            course.created_by = admin  # Set the creator as the logged-in user
            course.save()
            form.save_m2m()  # Save the ManyToManyField relationships

            modules = formset.save(commit=False)
            for module in modules:
                module.course = course  # Link module to the course
                module.resource_link="https://www.youtube.com/embed/"+extract_video_id(module.resource_link)
                module.save()
            formset.save_m2m()  # Save the inline formset relationships
            employees = User.objects.filter(role=Role.objects.get(role_name='Employee').id)  # Filter users with the role 'employee'
            notification = Notification.objects.create(
                title=f"New Course: {course.title}",
                message=f"A new course titled '{course.title}' has been created.")
            notification.recipients.set(employees)  # Assign all employees as recipients
            return redirect('Admin',user_id=user_id)  # Redirect to the course list page after successful creation
            notification.recipients.set(employees)  # Assign all employees as recipients
    else:
        form = CourseCreationForm()
        formset = ModuleFormSet()

    return render(request, 'dashboards/create_course.html', {'form': form, 'formset': formset})


def view_course(request, course_id, user_id):
    course = get_object_or_404(Course, course_id=course_id)
    modules = course.modules.all()
    user = get_object_or_404(User, id=user_id)

    completed_modules_qs = ModuleCompletion.objects.filter(user=user, module__in=modules, is_completed=True)
    completed_modules_ids = set(completed_modules_qs.values_list('module__module_id', flat=True))
    total_modules = modules.count()
    completed_modules_count = completed_modules_qs.count()
    progress = int((completed_modules_count / total_modules) * 100) if total_modules > 0 else 0

    if request.method == 'POST':
        module_id = request.POST.get('module_id')
        try:
            module = get_object_or_404(Module, module_id=module_id)
            completion, created = ModuleCompletion.objects.get_or_create(user=user, module=module)
            completion.is_completed = not completion.is_completed
            completion.save()
        except Exception as e:
            print(f"Error: {e}")

        return HttpResponseRedirect(request.path)

    return render(request, 'dashboards/view_course.html', {
        'course': course,
        'modules': modules,
        'progress': progress,
        'completed_modules': completed_modules_ids,
    })


def feedback_view(request, course_id, user_id):
    # Retrieve the course and employee objects
    course = get_object_or_404(Course, course_id=course_id)
    employee = get_object_or_404(User, id=user_id)

    # If the request method is POST, process the feedback form
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Save the feedback with the associated course and employee (user)
            feedback = form.save(commit=False)  # Don't save yet
            feedback.course = course
            feedback.employee = employee
            feedback.save()  # Now save the feedback to the database
            
            # Redirect to a success page (can be course view page or a confirmation page)
            return redirect('view_course', course_id=course_id,user_id=user_id)
    else:
        # If the form was not submitted, render an empty form
        form = FeedbackForm()

    # Render the feedback form page
    return render(request, 'dashboards/feedback_form.html', {'form': form, 'course': course,'employee':employee})



def Employee_view(request, user_id):
    employee = get_object_or_404(User, id=user_id)

    # Handle feedback form submission
    if request.method == 'POST':
        form = GeneralFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = employee  # Assign the feedback to the employee
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('Employee', user_id=user_id)  # Redirect to the same page
    else:
        form = GeneralFeedbackForm()
    notifications = Notification.objects.filter(recipients=employee).order_by('-created_at')

    

    context = {
        'employee': employee,
        'courses': Course.objects.all(),
        'form': form,  # Include the form in the context
        'notifications': notifications
    }
    return render(request, 'dashboards/Employee.html', context)



def Manager_view(request, user_id):
    manager = get_object_or_404(User, id=user_id)
    training_requests = TrainingRequest.objects.filter(account_manager=manager).order_by('-created_at')
    limit = int(request.GET.get('limit', 5))
    offset = int(request.GET.get('offset', 0))


    # Use Paginator to manage data
    paginator = Paginator(training_requests, limit)
    page_number = offset // limit + 1
    page = paginator.get_page(page_number)
    
    context = {
        'name': manager.name,
        'total': training_requests.count(),
        'completed': training_requests.filter(status='Approved').count(),
        'pending': training_requests.filter(status='Pending').count(),
        'data': page,
    }

    if request.method == 'POST':
        form = TrainingRequestForm(request.POST)
        if form.is_valid():
            # Create a TrainingRequest instance but don't save it yet
            instance = form.save(commit=False)
            instance.account_manager = manager  # Set the account manager
            instance.save()  # Save the instance to the database
            return redirect("Manager", user_id=user_id)
        else:
            print(form.errors)  # Print errors for debugging
    else:
        form = TrainingRequestForm()

    context['form'] = form
    return render(request, 'dashboards/Manager.html', context)



def feedback_tracker(request,user_id):
    # Fetch course feedback and general feedback from the database
     # Get all course feedback data
    feedbacks = Feedback.objects.all().select_related('course', 'employee')

    # Get all general feedback data
    general_feedback_data = GeneralFeedback.objects.all().select_related('user')

    return render(request, 'dashboards/feedback_tracker.html', {
        'course_feedback_data': feedbacks,
        'general_feedback_data': general_feedback_data
    })