from django.db import models

# Create your models here.
from django.db import models

class JobPosition(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    experience_year = models.CharField(max_length=50)

class JobApplication(models.Model):
    applicant_name = models.CharField(max_length=100)
    applicant_email = models.EmailField()
    years_of_experience = models.DecimalField(max_digits=3, decimal_places=1)
    resume = models.FileField(upload_to='resumes/')
    position_applied = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
