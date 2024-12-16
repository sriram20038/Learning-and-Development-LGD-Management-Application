from django.db import models

class TrainingRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending')],  # Only 'Pending' by default
        default='Pending'
    )
    account_manager = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role__role_name': 'Manager'}
    )

    def __str__(self):
        return self.title
