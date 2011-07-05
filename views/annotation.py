from django.http import HttpResponse
from frat.models import Project, Page, Revision, Comment, Annotation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from frat.cloud_handlers import upload_cloud_file
from django.utils import simplejson

def save_annotations(request, user_name, project_slug, page_slug, revision_number):
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
