from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

def reports_list(request):
    # Example static data for now
    reports = [
        {"id": 1, "title": "Sales Report", "status": "Complete"},
        {"id": 2, "title": "User Growth", "status": "Pending"},
        {"id": 3, "title": "Revenue Analysis", "status": "Complete"},
    ]
    return JsonResponse(reports, safe=False)

def users_list(request):
    try:
        # Return all users with id and username
        users = list(User.objects.values("id", "username", "email"))
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def hello(request):
    return JsonResponse({"message": "Hello API is working!"})

