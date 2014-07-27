from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Count
from .forms import AddJobForm, PhoneNumberForm
from .models import Job, PhoneNumber, JobApplication
from django.contrib.auth.decorators import login_required

# Create your views here.
def job_list(request):
    if request.user.is_authenticated():                
        if request.user.profile.is_student:            
            job_applications = JobApplication.objects.filter(user=request.user)
            available_jobs = Job.objects.annotate(
                                            workers_found=Count('jobapplication')
                                       ).filter(
                                            workers_found__lt=F('workers_needed')
                                       ).exclude(
                                            id__in = job_applications.values_list('job__id', flat=True))
            return render(request, 'jobs/student/dashboard.html', { 'jobs': available_jobs, 'job_applications': job_applications })
        else:            
            jobs = Job.objects.filter(user=request.user)
            return render(request, 'jobs/job_list.html', { 'jobs': jobs })                
    else:
        return render(request, 'jobs/homepage.html')


@login_required
def add_job(request):
    if request.POST:
        job_form = AddJobForm(request.POST)
        phone_number_form = PhoneNumberForm(request.POST)
        if job_form.is_valid() and phone_number_form.is_valid():
            job = job_form.save(commit=False)
            job.user = request.user
            job.status = 'published'
            #Check phone number
            number = phone_number_form.save(commit=False)            
            try:                
                number = request.user.phonenumber_set.get(phone_number=number.phone_number, user=request.user)                
            except:
                if request.user.phonenumber_set.count() == 0:
                    number.primary = True
                number.user = request.user
                number.save()                
                
            job.phone_number = number
            job.save()               
            return redirect('jobs:detail', job_id=job.id)
    else:        
        try:
           address = request.user.job_set.order_by('-date_created')[0].address
        except:
            address = ''               
        
        job_form = AddJobForm(initial={'workers_needed': 1, 'address': address})
        
        try:
            number = request.user.phonenumber_set.get(primary=True)
        except:
            number = ''      
            
        phone_number_form = PhoneNumberForm(initial={'phone_number': number})
        
    return render(request, 'jobs/add_job.html', { 'job_form': job_form, 'phone_number_form': phone_number_form })


def detail(request, job_id):    
    job = get_object_or_404(Job, pk=job_id)
    user_applied = job.user_applied(request.user)
    current_user = request.user
    return render(request, 'jobs/job_details.html', { 'job': job, 'user_applied': user_applied, 'current_user': current_user })


def apply_for_job(request, job_id):
    if request.POST:
        job = get_object_or_404(Job, pk=job_id)
        if job.available:
            if not job.user_applied(request.user):
                application = JobApplication(job=job, user=request.user)
                application.save()                
        
    return redirect('jobs:detail', job_id=job.id)


def cancel_job_application(request, job_id):
    if request.POST:
        try:
            job = get_object_or_404(Job, pk=job_id)
            application = JobApplication.objects.get(user=request.user, job = job)
            application.delete()           
        except:
            pass
    return redirect('jobs:detail', job_id=job_id)


def my_jobs(request):
    jobs = Job.objects.filter(jobapplication__user=request.user)
    return render(request, 'jobs/job_list.html', { 'jobs': jobs })