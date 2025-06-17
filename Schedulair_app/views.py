from django.shortcuts import render, redirect
import json
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from .models import *
import datetime, calendar
from django.db.models import Q, Count

# Create your views here.

def timetable_context_data():
    # time-table for current day
    current_date = datetime.date.today()
    current_date_tt = Time_table.objects.filter(date = current_date)

    # time-table for current week
    week_start_date = current_date - datetime.timedelta(days=current_date.weekday())
    week_end_date = week_start_date + datetime.timedelta(days=6)
    week_tt = Time_table.objects.filter(date__range=(week_start_date, week_end_date))

    # time-table for current month
    month_start_date = current_date.replace(day=1)
    if current_date.month == 12:
        month_end_date = current_date.replace(year=current_date.year + 1, month=1, day=1) - datetime.timedelta(days=1)
    else:
        month_end_date = current_date.replace(month=current_date.month + 1, day=1) - datetime.timedelta(days=1)
    month_tt = Time_table.objects.filter(date__range=(month_start_date, month_end_date))

    # time-table for whole sem
    sem_tt = Time_table.objects.all()

    # exam days
    exam_tt = ExamSchedule.objects.all()

    # holiday 
    holidays = Holiday.objects.all()

    return current_date_tt, week_tt, month_tt, sem_tt, exam_tt, holidays

def attendance_context_data():
    subjects = list(Time_table.objects.values_list('class_name', flat=True).distinct())
    attendances = {}
    for subject in subjects:
        attendances[subject] = Attendance.attendance_summary(subject)

    # overall attendance percentage
    data = Attendance.objects.aggregate(
        total = Count('id'),
        present = Count('id', filter=Q(present = True))
    )
    overall_per = (data['present']/data['total'])*100

    return attendances, overall_per

def dashboard(request):
    # time table data
    current_date_tt, week_tt, month_tt, sem_tt, exam_tt, holidays = timetable_context_data()

    # assignment data
    assignments = Assignments.objects.filter(submitted = False)

    # project data
    projects = Projects.objects.filter(completed = False)

    # attendance data 
    attendances , overall_per= attendance_context_data()

    # for the underline under current day
    current_day = datetime.datetime.now().strftime("%A")
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # attendance updation 
    status = request.GET.get("status")
    class_id = request.GET.get("class_id")
    print(status, class_id)
    if status and class_id:
        try:
            if status == "attended":
                entry = Attendance.objects.get(id=class_id)
                entry.present = True
                entry.save()
            
            elif status == "absent":
                entry = Attendance.objects.get(id=class_id)
                if entry.present:
                    entry.present = False
                    entry.save()
                else:
                    pass

            elif status == "cancelled":
                entry = Attendance.objects.get(id=class_id)
                entry.delete()

            return redirect('dashboard')
        
        except Exception as e:
            print(e)


    context = {
        'current_date_tt' : current_date_tt,
        'week_tt' : week_tt,
        'week_days' : week_days,
        'current_day' : current_day,
        'month_tt' : month_tt,
        'sem_tt' : sem_tt,
        'exam_tt' : exam_tt,
        'holidays' : holidays,
        'assignments' : assignments,
        'projects' : projects,
        'attendances' : attendances,
        'overall_per' : overall_per,
    }

    return render(request, "dashboard.html", context=context)


def loginpage(request):
    return render(request, 'login.html')

def user_login(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST


            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                if request.content_type == "application/json":
                    return JsonResponse({"error": "Email and password are required"}, status=400)
                else:
                    return render(request, 'login.html', {'error' : "Email and password are required"})
        

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                if request.content_type == "application/json":
                    print("gets here ")
                    return JsonResponse({"user_id": user.id, "role" : user.role, "message": "Login successful"}, status=200)
                else:
                    return redirect('dashboard')
            else:
                return render(request, 'login.html', {
                'error': "Invalid email or password. Please try again."})
        
        else:
            return render(request, 'login.html')
    
    except Exception as e:
        if request.content_type == "application/json":
            return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)
        else:
            return render(request, 'login.html', {'error' : f'Internal server error : {str(e)}'})

def user_signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(name, email, password, confirm_password)

        if not name or not email or not password or not confirm_password:
            return render(request, 'login.html', {'error': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'login.html', {'error': 'Passwords do not match'})

        if Users.objects.filter(email=email).exists():
            return render(request, 'login.html', {'error': 'Email already exists'})

        user = Users.objects.create(username=name, email=email, role='user')
        user.set_password(password)
        user.save()

        login(request, user)  # Logs the user in
        return redirect('dashboard')

    return render(request, 'login.html')  

def subject_calender(request, subject):
    current_date = datetime.date.today()
    month = int(request.GET.get('month') or current_date.month)
    year = int(request.GET.get('year') or current_date.year)

    month_name = datetime.date(year, month, day=1).strftime("%B")

    month_start_date = datetime.date(year, month, 1)
    _, last_day = calendar.monthrange(year, month)
    month_end_date = datetime.date(year, month, last_day)

    attendances = Attendance.objects.filter(date__range=(month_start_date, month_end_date), time_table_entry__class_name=subject)
    exams = ExamSchedule.objects.filter(date__range=(month_start_date, month_end_date))
    holidays= Holiday.objects.filter(date__range=(month_start_date, month_end_date))
    subjects = list(Time_table.objects.values_list('class_name', flat=True).distinct())

    days = {day : "No Class" for day in range(month_start_date.day, month_end_date.day + 1)}
    for attendance in attendances:
        if attendance.present:
            days[attendance.date.day] = "Attended"
        else:
            days[attendance.date.day] = "Missed"
    
    for exam in exams:
        days[exam.date.day] = "Exam"
    for holiday in holidays:
        days[holiday.date.day] = "Holiday"

    context = {
        'subject' : subject,
        'subjects' : subjects,
        'days' : days.items(),
        'month' : month, 
        'month_name' : month_name,
        'year' : year,
        'prev_month' : (month - 1) if month > 1 else 12,
        'prev_year' : year if month > 1 else year - 1,
        'next_month' : (month + 1) if month < 12 else 1,
        'next_year' : year if month < 12 else year + 1,
    }

    return render(request, "subject_cal.html", context)