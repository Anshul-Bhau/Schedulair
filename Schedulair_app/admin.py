from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Time_table)
class Time_Table_Admin(admin.ModelAdmin):
    list_display = ('class_name', 'start_time', 'end_time', 'date', 'day', 'class_no')
    