from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
import hashlib
import json
from datetime import datetime
from .models import Candidate, AdminUser

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            qualification = request.POST.get('qualification')
            course = request.POST.get('course')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            
            # Create new candidate
            candidate = Candidate.objects.create(
                name=name,
                age=age,
                gender=gender,
                qualification=qualification,
                course=course,
                mobile=mobile,
                email=email
            )
            
            return JsonResponse({'status': 'success', 'message': 'Application submitted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Hardcoded admin credentials
        if username == 'prashu' and password == 'prashu@143':
            request.session['admin_logged_in'] = True
            request.session['admin_username'] = username
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'admin_login.html')
    
    return render(request, 'admin_login.html')

def dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    filter_date = request.GET.get('date', '')
    
    # Base queryset
    candidates = Candidate.objects.all().order_by('-id')
    
    # Apply filters
    if search_query:
        candidates = candidates.filter(
            models.Q(name__icontains=search_query) | 
            models.Q(mobile__icontains=search_query)
        )
    
    if filter_date:
        candidates = candidates.filter(date=filter_date)
    
    # Statistics
    total_count = Candidate.objects.count()
    today_count = Candidate.objects.filter(date=datetime.now().date()).count()
    mlt_count = Candidate.objects.filter(course__icontains='MLT').count()
    grd_count = Candidate.objects.filter(course__icontains='GRD').count()
    
    context = {
        'candidates': candidates,
        'total_count': total_count,
        'today_count': today_count,
        'mlt_count': mlt_count,
        'grd_count': grd_count,
        'search_query': search_query,
        'filter_date': filter_date,
    }
    
    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect('home')

def export_data(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="candidates_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Age', 'Gender', 'Qualification', 'Course', 'Mobile', 'Email', 'Date'])
    
    candidates = Candidate.objects.all().order_by('-id')
    for c in candidates:
        writer.writerow([c.id, c.name, c.age, c.gender, c.qualification, c.course, c.mobile, c.email, c.date])
    
    return response

# Import models for Q object
from django.db import models