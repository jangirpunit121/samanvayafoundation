from django.contrib import admin
from .models import Candidate, AdminUser

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'course', 'date', 'created_at']
    search_fields = ['name', 'mobile', 'email']
    list_filter = ['course', 'date']

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'created_at']
    search_fields = ['username']