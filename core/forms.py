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
        fields = ['name', 'severity', 'affected_hosts', 'description', 'impact',
                  'solution', 'reference', 'cvss_rating', 'proof_screenshot']

        widgets = {'name': forms.TextInput(attrs={'class': 'input-field issueName width-90', 'style': 'border:none;',
                                                  'placeholder': "Name"}),
                   'severity': forms.Select(attrs={'class': 'select-field issueSeverity'}),
                   'affected_hosts': forms.Textarea(attrs={'class': 't-area issueHosts', 'rows': '1',
                                                           'placeholder': 'Affected Hosts'}),
                   'description': forms.Textarea(attrs={'class': 't-area issueDescription', 'rows': '3',
                                                        'placeholder': 'Description'}),
                   'impact': forms.Textarea(attrs={'class': 't-area issueSummary', 'rows': '3',
                                                   'placeholder': 'Impact'}),
                   'solution': forms.Textarea(attrs={'class': 't-area issueSolution', 'rows': '3',
                                                     'placeholder': 'Solution'}),
                   'reference': forms.Textarea(attrs={'class': 't-area issueReference', 'rows': '1',
                                                      'placeholder': 'Reference'}),
                   'cvss_rating': forms.NumberInput(attrs={'class': 'input-field issueRating', 'min': 0.0, 'max': 10.0,
                                                           'step': 1.0, 'placeholder': "CVSS"}),
                   'proof_screenshot': forms.FileInput(attrs={'accept': 'image/*', 'onchange': "preview($(this))"})
                   }

        labels = {k: "" for k in fields}


IssueFormSet = inlineformset_factory(Cases, Issues, form=IssueForm, extra=1, can_delete=True)
