from django.shortcuts import render, redirect
import json
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse

# Create your views here.

def dashboard(request):
    return render(request, "dashboard.html")



# def loginpage(request):
#     return render(request, 'login.html')

# def user_login(request):
#     try:
#         if request.method == 'POST':
#             if request.content_type == 'application/json':
#                 data = json.loads(request.body)
#             else:
#                 data = request.POST


#             email = data.get("email")
#             password = data.get("password")

#             if not email or not password:
#                 if request.content_type == "application/json":
#                     return JsonResponse({"error": "Email and password are required"}, status=400)
#                 else:
#                     return render(request, 'login.html', {'error' : "Email and password are required"})
        

#             user = authenticate(request, username=email, password=password)

#             if user is not None:
#                 login(request, user)
#                 if request.content_type == "application/json":
#                     print("gets here ")
#                     return JsonResponse({"user_id": user.id, "role" : user.role, "message": "Login successful"}, status=200)
#                 else:
#                     return redirect('dashboard')
#             else:
#                 print("got stuck")
#                 return render(request, 'login.html', {
#                 'error': "Invalid email or password. Please try again."})
        
#         else:
#             return render(request, 'login.html')
    
#     except Exception as e:
#         if request.content_type == "application/json":
#             return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)
#         else:
#             return render(request, 'login.html', {'error' : f'Internal server error : {str(e)}'})

