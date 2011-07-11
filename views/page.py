from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from frat.forms import NewPageForm
from django.shortcuts import render
from frat.models import Project, Page, Revision
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from frat.cloud_handlers import remove_project_data, upload_cloud_file
from django.template.defaultfilters import slugify

@login_required
def view_page(request, user_name, project_slug, page_slug):
    user = request.user
    owner = User.objects.get(username=user_name)
    project = Project.objects.get(owner=owner, slug=project_slug)
    page = Page.objects.get(project=project, slug=page_slug)
    latest = Revision.objects.filter(page=page).order_by('-revision_number')[0]
    return render(request, 'page.html', {'page':page, 'latest':latest})

@login_required
def new_page(request, user_name, project_slug):
    user = request.user
    if request.POST:
        form = NewPageForm(request.POST, request.FILES)
        if form.is_valid():
            new_page = form.save(commit=False)
            owner = User.objects.get(username=user_name)
            new_page.project = Project.objects.get(owner=owner, slug=project_slug)
            new_page.slug = slugify(new_page.name)
            new_page.save()
            rev_file_name = upload_cloud_file(request.FILES['image_file'], user_name, project_slug, new_page.slug, 1)
            initial_revision = Revision(revision_number=1, page=new_page, media_file_name=rev_file_name)
            initial_revision.save()
            return HttpResponseRedirect('/%s/%s' % (user_name, project_slug))
    else:
        form = NewPageForm()
    return render(request, 'new.html', {'form':form, 'type':'page'})
