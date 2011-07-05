from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    #/projects/
    url(r'^all', 'frat.views.general.all_projects'),
    url(r'^recent', 'frat.views.general.recent_projects'),
    url(r'^approved', 'frat.views.general.approved_projects'),
    url(r'^new', 'frat.views.project.new_project'),
    
    
    #/user_name/project_name/
    url(r'^$', 'frat.views.project.view_project'),
    url(r'^remove$', 'frat.views.project.remove_project'),
    
    url(r'^media/(?P<object_name>.+)/$', 'frat.views.media.view_media'),
    
    url(r'^pages/new/$', 'frat.views.page.new_page'),
    url(r'^(?P<page_slug>[-\w]+)/$', 'frat.views.page.view_page'),
    
    url(r'^(?P<page_slug>[-\w]+)/revisions/new/$', 'frat.views.revision.new_revision'),
    url(r'^(?P<page_slug>[-\w]+)/(?P<revision_number>[-\w]+)/$', 'frat.views.revision.view_revision'),
    
    url(r'^(?P<page_slug>[-\w]+)/(?P<revision_number>[-\w]+)/annotations/new/', 'frat.views.annotation.save_annotations'),
    
)

