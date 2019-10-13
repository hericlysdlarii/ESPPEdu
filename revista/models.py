from django.db import models
from django.contrib.auth.models import User

class tasks(models.Model):
    PRIORITY_CHOICES = [
        ('H','Alta'),
        ('M','Média'),
        ('L','Alta')
    ]

    name = models.CharField(max_length=30, null=False, blank=False)
    about = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, null=False, blank=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)