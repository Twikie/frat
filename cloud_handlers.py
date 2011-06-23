from django.conf import settings
import cloudfiles

cloud_user = settings.CLOUD_USER
cloud_key = settings.CLOUD_KEY

#We upload a file every time we create a new revision
def upload_cloud_file( fd, username, project, page, revision ):
    #get a connection to the cloud
    connection = cloudfiles.get_connection(cloud_user, cloud_key)
    
    #Get the container we're adding files to. Containers are saved to cloudfiles with the name <username_projectname>
    container = connection.get_container('%s_%s' % (username, project) )
    
    #Make the container public, this allows us to have a public url for the objects within.
    #Set the ttl to a big number, because we don't need to edit our files
    container.make_public(ttl=604800)
    
    #Create the object with the name <pagename_revisionnumber_filename>
    ob = container.create_object('%s_%s_%s' % (page, revision, fd.name))
    ob.content_type = fd.content_type
    
    #loop through each chunk in the file and write them to the cloudfiles object
    for chunk in fd.chunks():
        ob.write(chunk)
    fd.close()
    
    #Get the public URI for later access of the object
    return ob.public_uri()


def create_cloud_container ( username, project ):
    connection = cloudfiles.get_connection(cloud_user, cloud_key)
    container = connection.create_container('%s_%s' % (username, project) )
    

def remove_cloud_file ( username, project, page, revision, filename ):
    connection = cloudfiles.get_connection(cloud_user, cloud_key)
    container = connection.get_container('%s_%s' % (username, project))
    container.delete_object('%s_%s_%s' % (page, revision, filename))


def remove_cloud_container ( username, project ):
    connection = cloudfiles.get_connection(cloud_user, cloud_key)
    connection.delete_container('%s_%s' % (username, project) )
