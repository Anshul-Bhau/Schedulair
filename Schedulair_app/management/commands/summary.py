from django.core.management import BaseCommand, commands
from Schedulair_app.models import *

class Command(BaseCommand):
    help="to get the summaries of differnt tables - Attendance, Assignments and Projects"

    def handle(self, *args, **kwargs):
        try:
            print("For projects -", Projects.projects_summary())
            print("For assignments -", Assignments.assignment_summary())
            sub = input("Enter the subject to get attendance summary for :")
            if sub not in list(Time_table.objects.values_list('class_name', flat=True).distinct()):
                self.stdout.write(self.style.WARNING("Please enter a valid subject name"))
                return
            
            print("For attendance -", Attendance.attendance_summary(sub))

            self.stdout.write(self.style.SUCCESS("Summaries successfully shown"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occured - {e}"))