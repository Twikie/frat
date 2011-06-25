from django.contrib.auth.models import User
from frat.models import Project
from frat.cloud_handlers import get_object_data
from django.http import HttpResponse

def view_media(request, user_name, project_name, object_name):
    project_owner = User.objects.get(username=user_name)
    project = Project.objects.get(owner=project_owner, name=project_name)
    
    #If the user is the owner, or on the member's list. They can see this image
    if ( not project.is_private or request.user == project_owner or project.members.filter(username=request.user.username).count() > 0 ):  
        obj = get_object_data(user_name, object_name)
        return HttpResponse(obj.read(), mimetype=obj.content_type)
    return HttpResponseForbidden('Forbidden')
