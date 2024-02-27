from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login')
def positions(request):
    context={}
    if request.method=='POST':
        experience=request.POST.get('exp')
        role=JobPosition.objects.filter(experience_year=experience)
        context['position']=role
        
    else:
        role=JobPosition.objects.all()
        context['position']=role
    return render(request, 'positions.html', context)

def apply(request,id):
    role=JobPosition.objects.get(id=id)
    if request.method=='POST':
        applicat_name=request.POST.get('name')
        applicat_email=request.POST.get('email')
        years_of_experience=request.POST.get('exp')
        resume = request.FILES['resume']
        
        new_data=JobApplication(applicant_name=applicat_name, applicant_email=applicat_email, years_of_experience=years_of_experience, resume=resume, position_applied=role)
        if new_data is not None:
            new_data.save()
        subject = 'Message from Job Application System.'
        message = f'your request is submitted successfully for the position {role.title}. Our Team contact u shortly.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [applicat_email, ]
        send_mail(subject, message, email_from, recipient_list)
        
        subject=f'Requesting from {applicat_name}.'
        message=f'Reqest from {applicat_name} for the position of {role.title}. Total Experience is {years_of_experience} years.'
        mail = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, ['altaf.123.it@gmail.com'])
        mail.attach(resume.name, resume.read(), resume.content_type)
        mail.send()
          
    return render(request, 'apply.html',{'role':role})

def register(request):
    if request.method=='POST':
        first_name=request.POST.get('fname')
        last_name=request.POST.get('lname')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password1=request.POST.get('pass1')
        password2=request.POST.get('pass2')
        
        if password1==password2:
            User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
            return redirect('/login')
        
        
    return render(request, 'register.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/position')
        else:
            return HttpResponse('invalid cridential')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')