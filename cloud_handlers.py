from django.conf import settings
import cloudfiles

def upload_cloud_file( fd, user, project, page, revision ):
    cloud_user = settings.CLOUD_USER
    cloud_key = settings.CLOUD_KEY
    cloud_container = 'images'
    
    connection = cloudfiles.get_connection(cloud_user, cloud_key)
    container = connection.create_container('%s_%s' % (user, project))
    container.make_public(ttl=604800)
    #open a file and write the descriptor
    ob = container.create_object('%s_%s_%s' % (page, revision, fd.name) )
    ob.content_type = fd.content_type
    for chunk in fd.chunks():
        ob.write(chunk)
    fd.close()
    return ob.public_uri()
