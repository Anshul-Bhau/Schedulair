from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime, timedelta
from Schedulair_app.models import *

class Command(BaseCommand):
    help = "Populate timetable entries for the semester and create attendance instances"
    
    def handle(self, *args, **options):
        sem_start_date = ""
        sem_end_date = ""

        sem_start_date=input("Enter the semester start date :")
        sem_end_date= input("Enter the semester end date :")

        sem_start_date = datetime.strptime(sem_start_date, "%Y-%m-%d").date()
        sem_end_date = datetime.strptime(sem_end_date, "%Y-%m-%d").date()

        manual_week_start = sem_start_date
        manual_week_end = sem_start_date + timedelta(days=6)

        original_week_data = Time_table.objects.filter(date__range=(manual_week_start, manual_week_end))
        if not original_week_data.exists():
            self.stdout.write(self.style.WARNING("No timetable data found for the first week."))
            return
        # Create attendance instances for the first week
        for entry in original_week_data:
            if not Attendance.objects.filter(date=entry.date, time_table_entry=entry).exists():
                Attendance.objects.create(
                        time_table_entry=entry,
                        date=entry.date,
                        present=False,
                        )
        
        # add 7 days as the data for first week is already added
        week_start = manual_week_start + timedelta(days=7)
        week_index = 1

        while week_start <= sem_end_date:
            with transaction.atomic():
                for entry in original_week_data:
                    new_date = entry.date + timedelta(weeks=week_index)
                    if new_date > sem_end_date:
                        continue
                    if not Time_table.objects.filter(date=new_date, class_name = entry.class_name).exists():
                        new_entry = Time_table.objects.create(
                            day=entry.day,
                            class_name = entry.class_name,
                            subject_teacher = entry.subject_teacher,
                            class_no = entry.class_no,
                            class_room_no = entry.class_room_no,
                            start_time = entry.start_time,
                            end_time = entry.end_time,
                            date = new_date,
                        )
                    if not Attendance.objects.filter(date=new_date, time_table_entry = new_entry).exists():
                        Attendance.objects.create(
                            time_table_entry = new_entry,
                            date = new_date,
                            present = False,
                        )

            week_index += 1
            week_start += timedelta(weeks=1)

        self.stdout.write(self.style.SUCCESS("Timetable populated for the entire semester."))