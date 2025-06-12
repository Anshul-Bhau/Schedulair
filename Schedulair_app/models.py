from django.db import models, transaction
from datetime import datetime, timedelta



def start_time_choices():
        slots = []
        start="08:30"
        end="14:30"
        start_dt = datetime.strptime(start, "%H:%M")
        end_dt = datetime.strptime(end, "%H:%M")

        while start_dt <= end_dt:
            start_time = start_dt.strftime('%H:%M')
            slots.append((start_time, start_time))
            start_dt += timedelta(minutes=60)
        
        return slots
    
def end_time_choices():
    slots = start_time_choices()
    slots.append(('15:30', '15:30'))
    slots = [slot for slot in slots if slot[0] != '08:30']
    # slots.remove(('8:30', '8:30'))
    return slots


class Time_table(models.Model):     # instances of each day
    day_choices = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    day = models.CharField(choices=day_choices, null=False, blank=False, max_length=200)
    class_name = models.TextField(null=False, blank=False, default="Break")
    subject_teacher = models.CharField(max_length=250, null=True, blank=True)
    class_no = models.IntegerField() # in which period the class takes place
    class_room_no = models.CharField(max_length=100)
    start_time = models.CharField(choices=start_time_choices(), max_length=200)
    end_time = models.CharField(choices=end_time_choices(), max_length=200)
    date = models.DateField()

    def populate_attendace_records(self):
        Attendance.objects
        

class Attendance(models.Model):
    time_table_entry = models.ForeignKey(Time_table, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    def attendance_summary(self, subject):
        return Attendance.objects.filter(class_name = subject).aggregate(
            total=models.Count('id'),
            present=models.Count('id', filter=models.Q(present=True)),
            absent=models.Count('id', filter=models.Q(present=False))
        )

class Assignments(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False, default="Assignment")
    subject = models.CharField(max_length=250, null=False, blank=False)
    issue_date = models.DateTimeField()
    submission_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    
    def assignment_summary(self):
        return Assignments.objects.all().aaggregate(
            total = models.Count('id'),
            completed= models.Count('id', filter=models.Q(completed=True)),
            incomplete = models.Count('id', filter=models.Q(completed=False)),
            submitted = models.Count('id', filter=models.Q(submitted=True)),
            not_submitted= models.Count('id', filter=models.Q(submitted=False))
        )