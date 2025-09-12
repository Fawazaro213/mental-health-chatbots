# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UniversityStudent, UserProfile, Notification

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'preferred_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'has_mental_health_history', 'allow_data_collection', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'preferred_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Information', {
            'fields': ('date_of_birth', 'preferred_name', 'emergency_contact')
        }),
        ('Mental Health Settings', {
            'fields': ('has_mental_health_history',)
        }),
        ('Privacy Settings', {
            'fields': ('allow_data_collection',)
        }),
    )

@admin.register(UniversityStudent)
class UniversityStudentAdmin(admin.ModelAdmin):
    list_display = ('matric_number', 'first_name', 'last_name', 'faculty', 'department', 'year_admitted')
    list_filter = ('faculty', 'department', 'year_admitted')
    search_fields = ('matric_number', 'first_name', 'last_name', 'email')
    ordering = ('matric_number',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_student_matric', 'last_mood_check', 'average_mood_score')
    list_filter = ('last_mood_check',)
    search_fields = ('user__username', 'user__email', 'student_record__matric_number')
    ordering = ('-last_mood_check',)
    
    def get_student_matric(self, obj):
        return obj.student_record.matric_number if obj.student_record else 'No Student Record'
    get_student_matric.short_description = 'Student Matric Number'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'get_message_preview', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('recipient__username', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def get_message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    get_message_preview.short_description = 'Message Preview'