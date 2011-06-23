from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    #/projects/
    url(r'^all', 'projects.views.index'),
    url(r'^new', 'projects.views.newproject'),
    
    
    #/user_name/project_name/
    url(r'^$', 'projects.views.project'),
    url(r'^pages/new/$', 'projects.views.newpage'),
    url(r'^(?P<page_name>\w+)/$', 'projects.views.page'),
    url(r'^(?P<page_name>\w+)/revisions/new/$', 'projects.views.newrevision'),
    url(r'^(?P<page_name>\w+)/(?P<revision_number>\w+)/$', 'projects.views.revision'),
)

