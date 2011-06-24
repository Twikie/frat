from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    #/projects/
    url(r'^all', 'frat.views.index'),
    url(r'^new', 'frat.views.newproject'),
    
    
    #/user_name/project_name/
    url(r'^$', 'frat.views.project'),
    url(r'^pages/new/$', 'frat.views.newpage'),
    url(r'^(?P<page_name>\w+)/$', 'frat.views.page'),
    url(r'^(?P<page_name>\w+)/revisions/new/$', 'frat.views.newrevision'),
    url(r'^(?P<page_name>\w+)/(?P<revision_number>\w+)/$', 'frat.views.revision'),
    url(r'^(?P<page_name>\w+)/(?P<revision_number>\w+)/annotations/new/', 'frat.views.saveAnnotations'),
)

