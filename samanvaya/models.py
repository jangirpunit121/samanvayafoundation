from django.db import models

class Candidate(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    COURSE_CHOICES = [
        ('MLT (Medical Lab Technology)', 'MLT (Medical Lab Technology)'),
        ('GRD (General Radiology & Diagnosis)', 'GRD (General Radiology & Diagnosis)'),
    ]
    
    QUALIFICATION_CHOICES = [
        ('10th Pass', '10th Pass'),
        ('12th Pass', '12th Pass'),
        ('B.Sc', 'B.Sc'),
        ('B.Com', 'B.Com'),
        ('B.A', 'B.A'),
        ('M.Sc', 'M.Sc'),
        ('M.Com', 'M.Com'),
        ('M.A', 'M.A'),
    ]
    
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES)
    course = models.CharField(max_length=255, choices=COURSE_CHOICES)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.course}"

class AdminUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username