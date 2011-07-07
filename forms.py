from django import forms

from frat.models import *

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner', 'slug')

class NewRevisionForm(forms.ModelForm):
    image_file = forms.FileField()    
    class Meta:
        model = Revision
        exclude = ('page', 'media_file_name', 'slug', 'revision_number')
        
        
class NewPageForm(forms.ModelForm):
    image_file = forms.FileField()
    class Meta:
        model = Page
        exclude = ('project', 'is_approved', 'slug')
