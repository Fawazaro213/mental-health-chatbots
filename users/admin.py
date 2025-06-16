# # users/admin.py
# from django.contrib import admin
# from .models import UniversityStudent

# @admin.register(UniversityStudent)
# class UniversityStudentAdmin(admin.ModelAdmin):
#     list_display = ('matric_number', 'first_name', 'last_name', 'faculty', 'department', 'is_active')
#     list_filter = ('faculty', 'department', 'year_admitted', 'is_active')
#     search_fields = ('matric_number', 'first_name', 'last_name', 'email')
#     ordering = ('matric_number',)