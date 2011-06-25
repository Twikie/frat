from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from frat.forms import NewRevisionForm
from django.shortcuts import render
from frat.models import Project, Page, Revision, Comment, Annotation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from frat.cloud_handlers import upload_cloud_file
from django.utils import simplejson

@login_required
def view_revision(request, user_name, project_name, page_name, revision_number):
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
        ann_item['author'] = ann.author.username
        ann_list.append(ann_item)
    
    annotations = simplejson.dumps( ann_list )
    return render(request, 'revision.html', {'revision':revision, 'comments':comments, 'annotation_set': annotation_set, 'annotations':annotations})


@login_required
def new_revision(request, user_name, project_name, page_name):
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
    return render(request, 'new.html', {'form':form, 'type':'revision'})
