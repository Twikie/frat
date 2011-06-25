from django.conf import settings

from django.contrib.auth.models import User
from frat.models import Project, Page, Revision

import cloudfiles

cloud_user = settings.CLOUD_USER
cloud_key = settings.CLOUD_KEY

#We upload a file every time we create a new revision
def upload_cloud_file( fd, username, project, page, revision ):

    obj_file_name = '%s_%s_%s_%s' % (project, page, revision, fd.name)

    #get a connection to the cloud
    connection = cloudfiles.get_connection(cloud_user, cloud_key)
    
    #Get the container we're adding files to. Containers are saved to cloudfiles with the name <username_projectname>
    container = connection.get_container( username )
    
    #Create the object with the name <pagename_revisionnumber_filename>
    ob = container.create_object( obj_file_name )
    ob.content_type = fd.content_type
    
    #loop through each chunk in the file and write them to the cloudfiles object
    ob.write(fd.read())
    
    fd.close()
    
    #Get the object name for later access
    return obj_file_name


def create_cloud_container ( username ):
    connection = cloudfiles.get_connection(cloud_user, cloud_key)
    container = connection.create_container( username )
    

def remove_cloud_file ( username, filename ):
    connection = cloudfiles.get_connection(cloud_user, cloud_key)
    container = connection.get_container( username )
    container.delete_object( filename )


def remove_cloud_container ( username ):
    connection = cloudfiles.get_connection(cloud_user, cloud_key)
    connection.delete_container('%s' % username )
    
def remove_project_data ( project ):
    pages = Page.objects.filter(project=project)
    for page in pages:
        remove_page_data ( page )
        
def remove_page_data ( page ):
    revisions = Revision.objects.filter(page=page)
    for revision in revisions:
        remove_cloud_file( page.project.owner.username, revision.media_file_name )
    
#returns the amount of space being used in bytes by a specified user
def space_used_by_user ( username ):
    connection = cloudfiles.get_connection(cloud_user, cloud_key)
    return connection.get_container( username ).size_used
    
def get_object_data (username, filename):
    connection = cloudfiles.get_connection(cloud_user, cloud_key)
    container = connection.get_container( username )
    return container.get_object( filename )
     
    
    
