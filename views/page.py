from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from frat.forms import NewPageForm
from django.shortcuts import render
from frat.models import Project, Page, Revision
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from frat.cloud_handlers import remove_project_data

@login_required
def view_page(request, user_name, project_name, page_name):
    user = request.user
    page_name = page_name.replace('_', ' ')
    owner = User.objects.get(username=user_name)
    project = Project.objects.get(owner=owner, name=project_name)
    page = Page.objects.get(project=project, name=page_name)
    revisions = Revision.objects.filter(page=page)
    return render(request, 'page.html', {'page':page, 'revisions': revisions})

@login_required
def new_page(request, user_name, project_name):
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
    return render(request, 'new.html', {'form':form, 'type':'page'})
