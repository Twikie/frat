from django import forms

from frat.models import *

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner', 'slug')

class NewRevisionForm(forms.ModelForm):
    ffile = forms.FileField()    
    class Meta:
        model = Revision
        exclude = ('page', 'media_file_name', 'slug')
        
        
class NewPageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ('project', 'is_approved', 'slug')
