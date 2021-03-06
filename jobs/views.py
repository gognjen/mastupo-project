from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from .forms import AddJobForm, PhoneNumberForm
from .models import Job, PhoneNumber, JobApplication, ExternalJob

from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods

from lxml import html
import urllib2
from django.template.defaultfilters import slugify

import re
from datetime import datetime

@require_http_methods(["GET", "POST"])
@xframe_options_exempt
def home(request):
    if request.user.is_authenticated():                
        if request.user.profile.is_student:            
            job_applications = JobApplication.objects.filter(user=request.user)
            available_jobs = Job.objects.annotate(
                                            workers_found=Count('jobapplication')
                                       ).filter(
                                            workers_found=0, parent_id=0
                                       ).exclude(
                                            id__in = job_applications.values_list('job__id', flat=True))
            return render(request, 'jobs/student/dashboard.html', { 'jobs': available_jobs, 'job_applications': job_applications })
        else:            
            jobs = Job.objects.filter(user=request.user, parent_id=0, status='published')
            return render(request, 'jobs/dashboard.html', { 'jobs': jobs })         
    else:
        
        external_jobs = ExternalJob.objects.all().order_by('-date_published')
        
        return render(request, 'jobs/homepage.html', { 'external_jobs': external_jobs })

def about(request):
    return render(request, 'jobs/about.html')

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
            messages.success(request, _("Job posted successfully."))
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

@login_required
def job_edit(request, job_id=None):
    
    job = get_object_or_404(Job, pk=job_id)
    
    if job.user != request.user:
        return redirect('home')
    
    print request.POST
    
    if request.POST:
        job_form = AddJobForm(request.POST, instance=job)
        phone_number_form = PhoneNumberForm(request.POST, instance=job.phone_number)
        if job_form.is_valid() and phone_number_form.is_valid():
            
            backup_job = Job(
                description = job.description,
                price = job.price,
                date_created = job.date_created,
                date_modified = job.date_modified,
                user = job.user,
                phone_number = job.phone_number,
                status = job.status,
                address = job.address,
                parent_id = job.id
            )        
            backup_job.save()        
                    
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
        job_form = AddJobForm(instance=job)                           
        phone_number_form = PhoneNumberForm(instance=job.phone_number)
        
    return render(request, 'jobs/job_edit.html', { 'job_form': job_form, 'phone_number_form': phone_number_form })




def detail(request, job_id):    
    job = get_object_or_404(Job, pk=job_id)
    user_applied = job.user_applied(request.user)
    current_user = request.user
    return render(request, 'jobs/job_details.html', { 'job': job, 'user_applied': user_applied, 'current_user': current_user })

def job_delete(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    if job.user != request.user:
        return redirect('home')
    
    print request.POST
    
    if request.POST:               
        
        backup_job = Job(
            description = job.description,
            price = job.price,
            date_created = job.date_created,
            date_modified = job.date_modified,
            user = job.user,
            phone_number = job.phone_number,
            status = job.status,
            address = job.address,
            parent_id = job.id
        )        
        backup_job.save()        
        job.status = 'canceled'
        job.save()        
        
        return redirect('home')
    else:
        return render(request, 'jobs/job_delete.html', { 'job': job })
        

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
          

def external_detail(request, job_id):    
    job = get_object_or_404(ExternalJob, pk=job_id)    
    return render(request, 'jobs/external_job_details.html', { 'job': job })


def external_jobs(request):
    
    if request.POST:
        
        next_page = ['http://posao.banjaluka.com/?page_id=4']
        items = []       

        while next_page:
            
            req = urllib2.Request(next_page[0])
            req.add_header('User-agent', 'Mozilla 5.10')
            res = urllib2.urlopen(req)
            page = res.read().decode('utf-8')    
            res.close()
        
            tree = html.fromstring(page)           
               
            titles = tree.xpath('//*[@id="single-post"]/form/div/div/div/h3/a/text()')
            external_links = tree.xpath('//*[@id="single-post"]/form/div/div/div/h3/a/@href')
            locations = tree.xpath('//*[@id="single-post"]/form/div/div/div/h4/text()')
            employers = tree.xpath('//*[@id="single-post"]/form/div/div/div/p[1]/text()')
            categories = tree.xpath('//*[@id="single-post"]/form/div/div/div/p[2]/a/text()')            
            dates = tree.xpath('//*[@id="single-post"]/form/div/div/div/p[3]/text()')
            
            for title, link, location, employer, category, date in zip(titles, external_links, locations, employers, categories, dates):            
                parsed_dates = re.findall(r'\d{2}.\d{2}.\d{4}.', date)
                published = datetime.strptime(parsed_dates[0], "%d.%m.%Y.").date()
                expire = datetime.strptime(parsed_dates[1], "%d.%m.%Y.").date()
            
                try:
                    job = ExternalJob.objects.get(link=link)
                except ExternalJob.DoesNotExist:
                    job = ExternalJob(source="posao.banjaluka.com", title=title, location=location, link=link, employer=employer, category=category, date_expire=expire, date_published=published)           
                    job.save()                        
    
            next_page = tree.xpath('//*[@id="single-post"]/form/div/div[7]/div[3]/a/@href')
            
        return redirect('jobs:external_jobs')
        
    else:                   
        
        items = ExternalJob.objects.all().order_by('-date_published')
                        
        return render(request, 'jobs/external_jobs.html', { 'items': items, 'jobs' : [] })
