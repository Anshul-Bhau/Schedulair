from django.shortcuts import render, redirect
import json
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from .models import *

# Create your views here.

def dashboard(request):
    return render(request, "dashboard.html")

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

# def user_signup(request):
#     if request.method == "POST":
#         try:  
#             if request.content_type == 'application/json':
#                 data = json.loads(request.body)
#                 print("json data", data)
#             else:
#                 data = request.POST

#             name = data.get('name')
#             email = data.get('email')
#             password = data.get('password')
            
#             if not name or not email or not password:
#                 return JsonResponse({'error': 'All fields are required'}, status=400)

#             if Users.objects.filter(email = email).exists():
#                 return JsonResponse({'error': 'Email already in use'}, status=400)
            
#             user = Users.objects.create(username = name, email=email, role='user')
#             user.set_password(password)
#             user.save()

#             user = authenticate(request, username=email, password=password)
#             print("user made ", user)

#             print("going for js shii")
#             return JsonResponse({"user_id": user.id, "role" : user.role, "message": "Signup successful"}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)

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