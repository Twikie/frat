from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from frat.forms import NewProjectForm
from django.shortcuts import render
from frat.models import Project, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from frat.cloud_handlers import remove_project_data
from datetime import datetime, timedelta, date

def all_projects(request):
    projects = Project.objects.filter( Q(owner=request.user) | Q(members=request.user) )
    return render(request, 'index.html', {'projects': projects, 'type': 'all'})
    
def recent_projects(request):
    startdate = date.today() - timedelta(days=21)
    enddate = date.today() + timedelta(days=1)
    projects = Project.objects.filter( ( Q(owner=request.user) | Q(members=request.user) ) & Q(created_at__range=[startdate, enddate]) )
    return render(request, 'index.html', {'projects': projects, 'type': 'recent' })
    
def approved_projects(request):
    projects = Project.objects.filter( Q(owner=request.user) | Q(members=request.user) )
    return render(request, 'index.html', {'projects': projects, 'type': 'approved' })
