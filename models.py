from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    owner = models.ForeignKey(User)
    members = models.ManyToManyField(User, related_name="Project")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    is_private = models.BooleanField()
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    class Meta:
        unique_together = ("owner", "name")
    def __unicode__(self):
        return self.name
        
class Page(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project)
    created_at = models.DateTimeField(auto_now_add = True)
    is_approved = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    class Meta:
        unique_together = ("project", "name")
        
class Revision(models.Model):
    page = models.ForeignKey(Page)
    revision_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    media_file_name = models.URLField()
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    class Meta:
        unique_together = ("page", "revision_number")

class Annotation(models.Model):
    revision = models.ForeignKey(Revision)
    author = models.ForeignKey(User)
    x = models.IntegerField()
    y = models.IntegerField()
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)
    def __unicode__(self):
        return self.text

class Comment(models.Model):
    revision = models.ForeignKey(Revision)
    author = models.ForeignKey(User)
    reply_to = models.ForeignKey('self', null=True)
    text = models.CharField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)
