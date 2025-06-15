from django.db import models, transaction
from datetime import datetime, timedelta
from django.db.models import Q, Count
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
import uuid


class Users(AbstractUser):
    Role_Choices = [
        ("admin", "admin"),
        ("user", "user")
    ]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=225, null=False, blank=False, unique=False)
    email = models.EmailField(max_length=250, null=False, blank=False, unique=True)
    role = models.CharField(max_length=30, blank=False, null=False, choices=Role_Choices)
    user_created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=250, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'username', 'password']
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


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
    class_no = models.IntegerField(null=True, blank=True) # in which period the class takes place
    class_room_no = models.CharField(max_length=100)
    start_time = models.CharField(choices=start_time_choices(), max_length=200)
    end_time = models.CharField(choices=end_time_choices(), max_length=200)
    date = models.DateField()

class ExamSchedule(models.Model):
    subject = models.CharField(max_length=255)
    exam_name = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_no = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            Time_table.objects.filter(date=self.date).delete()

    def __str__(self):
        return f"{self.subject} - {self.exam_name} on {self.date}"

class Holiday(models.Model):
    date = models.DateField()
    reason = models.TextField()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            Time_table.objects.filter(date=self.date).delete()

    def __str__(self):
        return f"{self.date} - Holiday - {self.reason}"

class Attendance(models.Model):
    time_table_entry = models.ForeignKey(Time_table, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    @classmethod
    def attendance_summary(cls, subject):
        return cls.objects.filter(time_table_entry__class_name = subject).aggregate(
            total=Count('id'),
            present_count=Count('id', filter=Q(present=True)),
            absent_count=Count('id', filter=Q(present=False)),
            percentage = ((Count('id', filter=Q(present=True)))/(Count('id')))*100 
        )
    
    def __str__(self):
        return f"{self.time_table_entry.class_name} on {self.date} - {'present' if (self.present == True) else 'absent'}"

class Assignments(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False, default="Assignment")
    subject = models.CharField(max_length=250, null=False, blank=False)
    issue_date = models.DateTimeField()
    submission_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    
    @classmethod
    def assignment_summary(cls):
        return cls.objects.all().aggregate(
            total = Count('id'),
            completed_count= Count('id', filter=Q(completed=True)),
            incomplete_count = Count('id', filter=Q(completed=False)),
            submitted_count = Count('id', filter=Q(submitted=True)),
            not_submitted_count= Count('id', filter=Q(submitted=False))
        )
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class Projects(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)
    start_date = models.DateField()
    deadline = models.DateField()
    description = models.TextField(null=False)
    completed = models.BooleanField(default=False)

    @classmethod
    def projects_summary(cls):
        return cls.objects.all().aggregate(
            total = Count('id'),
            completed_count = Count('id', filter=Q(completed=True))
        )
    
    def __str__(self):
        return f"{self.name} - {self.description}"
    
# print(Projects.projects_summary())
# print(Attendance.attendance_summary("HV"))
# print(Assignments.assignment_summary())