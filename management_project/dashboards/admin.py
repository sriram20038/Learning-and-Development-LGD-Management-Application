from django.contrib import admin
from .models import TrainingRequest

@admin.register(TrainingRequest)
class TrainingRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'title', 'status', 'account_manager')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    actions = ['approve_requests', 'reject_requests']

    @admin.action(description='Approve selected training requests')
    def approve_requests(self, request, queryset):
        queryset.update(status='Approved')

    @admin.action(description='Reject selected training requests')
    def reject_requests(self, request, queryset):
        queryset.update(status='Rejected')
