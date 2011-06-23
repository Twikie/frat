from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from projects.models import *
from projects.forms import *

from projects.cloud_handlers import upload_cloud_file

def index(request):
    projects = Project.objects.all()
    return render_to_response('index.html', {'projects': projects})

@login_required
def newproject(request):
    user = request.user
    if request.POST:
        form = NewProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = user
            new_project.save()
            form.save_m2m()
            return HttpResponseRedirect('/%s/%s' % (user, new_project))
    else:
        form = NewProjectForm()
    return render_to_response('new.html', {'form': form, 'type':'project'}, context_instance=RequestContext(request))
    
@login_required
def newpage(request, user_name, project_name):
    user = request.user
    if request.POST:
        form = NewPageForm(request.POST)
        if form.is_valid():
            new_page = form.save(commit=False)
            owner = User.objects.get(username=user_name)
            new_page.project = Project.objects.get(owner=owner, name=project_name)
            new_page.save()
            return HttpResponseRedirect('/%s/%s' % (user_name, project_name))
    else:
        form = NewPageForm()
    return render_to_response('new.html', {'form':form, 'type':'page'}, context_instance=RequestContext(request))

@login_required
def newrevision(request, user_name, project_name, page_name):
    user = request.user
    if request.POST:
        form = NewRevisionForm(request.POST, request.FILES)
        if form.is_valid():
            new_revision = form.save(commit=False)
            owner = User.objects.get(username=user_name)
            project = Project.objects.get(owner=owner, name=project_name)
            new_revision.page = Page.objects.get(project=project, name=page_name)
            new_revision.image_url = upload_cloud_file(request.FILES['ffile'], user_name, project_name, page_name, new_revision.revision_number)
            new_revision.save()
            return HttpResponseRedirect('/%s/%s/%s' % (user_name, project_name, page_name))
    else:
        form = NewRevisionForm()
    return render_to_response('new.html', {'form':form, 'type':'revision'}, context_instance=RequestContext(request))
    
@login_required
def project(request, user_name, project_name):
    user = request.user
    owner = User.objects.get(username=user_name);
    project = Project.objects.get(owner=owner, name=project_name)
    pages = Page.objects.filter(project=project).order_by('-created_at')
    for page in pages:
        page.name = page.name.replace(' ', '_')
    return render_to_response('project.html', {'project': project, 'pages': pages});

@login_required
def page(request, user_name, project_name, page_name):
    user = request.user
    page_name = page_name.replace('_', ' ')
    owner = User.objects.get(username=user_name)
    project = Project.objects.get(owner=owner, name=project_name)
    page = Page.objects.get(project=project, name=page_name)
    revisions = Revision.objects.filter(page=page)
    return render_to_response('page.html', {'page':page, 'revisions': revisions})

@login_required
def revision(request, user_name, project_name, page_name, revision_number):
    page_name = page_name.replace('_', ' ')

    user = request.user
    
    owner = User.objects.get(username=user_name)
    project = Project.objects.get(owner=owner, name=project_name)
    page = Page.objects.get(project=project, name=page_name) 
    revision = Revision.objects.get(page=page, revision_number=revision_number)
    return render_to_response('revision.html', {'revision':revision})
