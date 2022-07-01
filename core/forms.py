from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from .models import Cases, Recon, Issues


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


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issues
        fields = ['name', 'summary', 'severity', 'description', 'reference', 'cvss_rating', 'proof_screenshot']

        widgets = {'name': forms.TextInput(attrs={'class': 'input-field', 'style':'border:none;', 'placeholder': "Name"}),
                   'summary': forms.Textarea(attrs={'class': 't-area', 'rows': '5', 'placeholder': 'Summary'}),
                   'severity': forms.Select(attrs={'class': 'select-field'}),
                   'description': forms.Textarea(attrs={'class': 't-area', 'rows': '3', 'placeholder': 'Description'}),
                   'reference': forms.Textarea(attrs={'class': 't-area', 'rows': '1', 'placeholder': 'Reference'}),
                   'cvss_rating': forms.NumberInput(attrs={'class': 'input-field', 'min': 0, 'max': 10, 'step': 1,
                                                           'placeholder': "CVSS"}),
                   'proof_screenshot': forms.FileInput(attrs={'accept': 'image/*', 'onchange': "preview($(this))"})
                   }

        labels = {k: "" for k in fields}


IssueFormSet = inlineformset_factory(Cases, Issues, form=IssueForm, extra=1, can_delete=True)
