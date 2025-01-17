from django import forms
from .models import TrainingRequest, Course, Feedback,GeneralFeedback,Module,Notification
from django.forms import inlineformset_factory

class TrainingRequestForm(forms.ModelForm):
    class Meta:
        model = TrainingRequest
        fields = ['title', 'description', 'course_duration', 'employee_count']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'status': forms.Select(),
        }

class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Course Description'}),
            'employees': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Course Title',
            'description': 'Course Description',
            'employees': 'Assign to Employees',
        }

# Inline formset for modules linked to a course
ModuleFormSet = inlineformset_factory(
    Course,
    Module,
    fields=('title', 'description', 'resource_link', 'file_upload'),
    widgets={
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Module Title'}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Module Description'}),
        'resource_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Resource Link'}),
        'file_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
    },
    extra=1,  # Default to 1 blank module form
    can_delete=True
)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'comments': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your comments here...', 
                'rows': 4
            }),
        }
        labels = {
            'course': 'Course',
            'rating': 'Rate the course (1 to 5)',
            'comments': 'Additional Comments',
        }



class GeneralFeedbackForm(forms.ModelForm):
    class Meta:
        model = GeneralFeedback
        fields = ['comments']  # Only the comments field is editable by the user
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your feedback'}),
        }
        labels = {
            'comments': 'Your Feedback',
        }


