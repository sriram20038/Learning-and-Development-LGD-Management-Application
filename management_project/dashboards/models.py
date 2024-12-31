from django.db import models

class TrainingRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'),
                 ('Approved', 'Approved'),
                 ('Rejected', 'Rejected')],
        default='Pending'
    )
    account_manager = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role__role_name': 'Manager'}
    )
    course_duration = models.PositiveIntegerField(help_text="Duration in days")  # New field
    employee_count = models.PositiveIntegerField(help_text="Number of employees involved")  # New field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    



# User model assumed to be in 'authentication' app
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role__role_name': 'Admin'},
        related_name='created_courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    employees = models.ManyToManyField(
        'authentication.User',
        related_name='enrolled_courses',
        limit_choices_to={'role__role_name': 'Employee'},
        blank=True
    )

    def number_of_modules(self):
        """Count the number of modules in this course."""
        return self.modules.count()

    def __str__(self):
        return self.title


class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    resource_link = models.URLField(max_length=1024, null=True, blank=True)
    file_upload = models.FileField(upload_to='module_resources/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class EmployeeCourseProgress(models.Model):
    employee = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role__role_name': 'Employee'},
        related_name='course_progress'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='progress'
    )
    progress_percentage = models.FloatField(default=0.0)  # Track course progress
    completed_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'course')

    def __str__(self):
        return f"{self.employee.username} - {self.course.title} ({self.progress_percentage}%)"




# Feedback Model
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)  # ForeignKey to Course
    employee = models.ForeignKey('authentication.User', on_delete=models.CASCADE)  # ForeignKey to User
    rating = models.IntegerField()  # IntegerField for ratings
    comments = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1) & models.Q(rating__lte=5), name='rating_between_1_and_5')
        ]

    def __str__(self):
        return f"Feedback ID: {self.feedback_id}, Course: {self.course}, Rating: {self.rating}"



class GeneralFeedback(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)  # User providing the feedback
    comments = models.TextField()  # Feedback comments
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp of submission

    def __str__(self):
        return f"Feedback by {self.user.name} on {self.submitted_at}"


class Notification(models.Model):
    title = models.CharField(max_length=255)  # Title of the notification
    message = models.TextField()  # Detailed notification message
    recipients = models.ManyToManyField('authentication.User', related_name='notifications')  # Users receiving the notification
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the notification was created
    is_read = models.BooleanField(default=False)  # Status of whether the notification has been read or not

    def __str__(self):
        return f"Notification: {self.title} ({self.created_at})"
    



class ModuleCompletion(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    module = models.ForeignKey('Module', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'module')