from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *

# Register your models here.
Users = get_user_model()
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')

@admin.register(Time_table)
class Time_Table_Admin(admin.ModelAdmin):
    list_display = ('class_name', 'start_time', 'end_time', 'date', 'day', 'class_no')
    ordering = ('date', )
    
@admin.register(Attendance)
class Attendance_Admin(admin.ModelAdmin):
    list_display = ('time_table_entry__class_name','time_table_entry__day', 'date', 'present')

@admin.register(Assignments)
class Assignment_Admin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'issue_date', 'submission_date', 'completed', 'submitted')

@admin.register(Projects)
class Project_Admin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'deadline', 'description', 'completed')