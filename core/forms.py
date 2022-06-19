from django import forms
from .models import Cases, Recon


class CaseForm(forms.ModelForm):
    class Meta:
        model = Cases
        fields = ['caseName', 'organization', 'caseLead',
                  'orgHandler', 'assessmentType', 'scope',
                  'logo']
        widgets = {
            'caseName': forms.TextInput(attrs={'class': 'input-field'}),
            'organization': forms.TextInput(attrs={'class': 'input-field'}),
            'caseLead': forms.TextInput(attrs={'class': 'input-field'}),
            'orgHandler': forms.TextInput(attrs={'class': 'input-field'}),
            'assessmentType': forms.RadioSelect(),
            'scope': forms.Textarea(attrs={'class': 't-area', 'rows': '5',
                                           'placeholder': 'Scope'}),
            'logo': forms.FileInput(attrs={'id': 'logo'})
        }
        labels = {
            'caseName': 'Case Name:',
            'organization': 'Organization:',
            'caseLead': 'Case Lead:',
            'orgHandler': 'Organization Handler:',
            'scope': 'Scope:',
            'logo': 'logo'
        }


class ReconForm(forms.ModelForm):
    class Meta:
        model = Recon
        fields = ['tools', 'passive_sources']
        widgets = {
            'tools': forms.HiddenInput(attrs={'required': False, 'id': 'json_tools',
                                              'name': 'json_tools'}),
            'passive_sources': forms.Textarea(attrs={'class': 't-area', 'rows': '5',
                                                     'placeholder': 'Data Sources'}),
        }
        labels = {
            'passive_sources': 'Data Sources',
        }
