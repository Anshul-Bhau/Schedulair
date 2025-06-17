from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *
from .resouces import *
from django import forms

# Register your models here.
Users = get_user_model()
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')

class Time_Table_AdminForm(forms.ModelForm):
    day = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Time_table
        fields = '__all__'
    
    

@admin.register(Time_table)
class Time_Table_Admin(admin.ModelAdmin):
    form = Time_Table_AdminForm
    resource_class = Time_table_Resource
    list_display = ('class_name', 'start_time', 'end_time', 'date', 'day', 'class_no')
    ordering = ('date', )

    def save_model(self, request, obj, form, change):
        if not obj.day and obj.date:
            obj.day = obj.date.strftime("%A")
        return super().save_model(request, obj, form, change)

@admin.register(Holiday)
class Holiday_Admin(admin.ModelAdmin):
    list_display = ('date', 'reason')
    ordering = ('date', )

@admin.register(ExamSchedule)
class Exam_Schedule_Admin(admin.ModelAdmin):
    list_display = ('exam_name', 'subject', 'start_time', 'end_time', 'date', 'room_no')
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