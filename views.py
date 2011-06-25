from django.utils import simplejson
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from frat.models import *
from frat.forms import *

from frat.cloud_handlers import upload_cloud_file, create_cloud_container, get_object_data

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
            create_cloud_container(user.username)
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
            new_revision.media_file_name = upload_cloud_file(request.FILES['ffile'], user_name, project_name, page_name, new_revision.revision_number)
            new_revision.save()
            return HttpResponseRedirect('/%s/%s/%s' % (user_name, project_name, page_name))
    else:
        form = NewRevisionForm()
    return render_to_response('new.html', {'form':form, 'type':'revision'}, context_instance=RequestContext(request))

def saveAnnotations(request, user_name, project_name, page_name, revision_number):
    user = request.user
    if request.is_ajax():
        if request.method == 'POST':
            if request.POST.__contains__('annotations'):
                revision_id = request.POST['revision']
                revision = Revision.objects.get(pk=revision_id)
                data = request.POST['annotations']
                annos = simplejson.loads(data)
                
                #Deletes all previous annotations
                Annotation.objects.filter(revision=revision).delete()
                
                #Add annotations currently on page
                for anno in annos:
                    #return HttpResponse(anno)
                    new_annotation = Annotation(author=user, revision=revision, x=anno['x'], y=anno['y'], text=anno['text'])
                    new_annotation.save()
                return HttpResponse('Saved Annotations')
    return HttpResponse('Nothing to see.')


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
    comments = Comment.objects.filter(revision=revision)
    
    annotation_set = Annotation.objects.filter(revision=revision)
    
    ann_list = []
    
    for ann in annotation_set:
        ann_item = dict()
        ann_item['x'] = ann.x
        ann_item['y'] = ann.y
        ann_item['text'] = ann.text
        ann_list.append(ann_item)
    
    annotations = simplejson.dumps( ann_list )
    return render_to_response('revision.html', {'revision':revision, 'comments':comments, 'annotations':annotations})
    
def viewmedia(request, user_name, project_name, object_name):
    project_owner = User.objects.get(username=user_name)
    project = Project.objects.get(owner=project_owner, name=project_name)
    
    #If the user is the owner, or on the member's list. They can see this image
    if ( not project.is_private or request.user == project_owner or project.members.filter(username=request.user.username).count() > 0 ):  
        obj = get_object_data(user_name, object_name)
        return HttpResponse(obj.read(), mimetype=obj.content_type)
    return HttpResponseForbidden('Forbidden')
