from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Personal_Information(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    date_of_birth=models.DateField(auto_now=False, auto_now_add=False)
    location=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=50)
    user=models.ForeignKey(User, on_delete=models.CASCADE)