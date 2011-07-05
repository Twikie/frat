from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from frat.forms import NewProjectForm
from django.shortcuts import render
from frat.models import Project, Page
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from frat.cloud_handlers import remove_project_data
from django.template.defaultfilters import slugify

@login_required
def view_project(request, user_name, project_slug):
    user = request.user
    owner = User.objects.get(username=user_name)
    project = Project.objects.get(owner=owner, slug=project_slug)
    pages = Page.objects.filter(project=project).order_by('-created_at')
    return render(request, 'project.html', {'project': project, 'pages': pages})

@login_required
def new_project(request):
    user = request.user
    if request.POST:
        form = NewProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = user
            new_project.slug = slugify(new_project.name)
            new_project.save()
            form.save_m2m()
            return HttpResponseRedirect('/%s/%s' % (user, new_project.slug))
    else:
        form = NewProjectForm()
    return render(request, 'new.html', {'form': form, 'type':'project'})

@login_required
def remove_project(request, user_name, project_slug):
    user = request.user
    owner = User.objects.get(username=user_name)
    if(user == owner):
        project = Project.objects.get(owner=owner, slug=project_slug)
        remove_project_data(project)
        project.delete()
    else:
        return HttpResponseForbidden('You must be the owner to remove this project')
    return HttpResponseRedirect('/%s' % user_name)
