from django.contrib import admin
from .models import TrainingRequest, Course, Module,EmployeeCourseProgress,Feedback,GeneralFeedback,ModuleCompletion

@admin.register(TrainingRequest)
class TrainingRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'title', 'status', 'account_manager', 'course_duration', 'employee_count', 'created_at')
    list_filter = ('status', 'account_manager', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'number_of_modules')
    list_filter = ('created_by', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    filter_horizontal = ('employees',)  # For ManyToManyField
    ordering = ('-created_at',)

    def number_of_modules(self, obj):
        return obj.number_of_modules()
    number_of_modules.short_description = 'Modules'


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'description', 'course__title')
    ordering = ('-created_at',)


@admin.register(EmployeeCourseProgress)
class EmployeeCourseProgressAdmin(admin.ModelAdmin):
    list_display = ('employee', 'course', 'progress_percentage', 'completed_on')
    list_filter = ('course', 'completed_on')
    search_fields = ('employee__username', 'course__title')
    ordering = ('-completed_on', 'progress_percentage')




@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'course', 'employee', 'rating', 'comments')
    search_fields = ('course__name', 'employee__username')  # Adjust based on actual fields in Course and User models
    list_filter = ('rating',)  # Filter by rating


@admin.register(GeneralFeedback)
class GeneralFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comments', 'submitted_at')  # Columns displayed in the admin list view
    list_filter = ('submitted_at',)  # Filters for the admin interface
    search_fields = ('user__username', 'comments')  # Fields for the search bar
    ordering = ('-submitted_at',)  # Default ordering by submission date (newest first)

    def get_queryset(self, request):
        # Customize the queryset if needed (e.g., for filtering by user permissions)
        return super().get_queryset(request).select_related('user')
    


class ModuleCompletionAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('user__username', 'module__name')
    list_editable = ('is_completed',)
    ordering = ('-is_completed',)

admin.site.register(ModuleCompletion, ModuleCompletionAdmin)
