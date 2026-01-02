from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    # Tech choices
    TECH_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('mern', 'MERN Stack'),
        ('php', 'PHP'),
        ('dotnet', '.NET'),
    ]

    # Link this profile to the logged-in User (One user = One Person entry)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    preferred_technology = models.CharField(max_length=10, choices=TECH_CHOICES)
    
    # This field controls your "lock" logic
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.preferred_technology}"