from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from .models import Cases, Recon, Issues, PoC


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
                  'solution', 'reference', 'cvss_rating']

        widgets = {'name': forms.TextInput(attrs={'class': 'input-field issueName width-90 pad-bottom',
                                                  'placeholder': "Name", 'id': '#issue-title'}),
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
                                                           'step': 0.1, 'placeholder': "CVSS"})
                   }

        labels = {k: "" for k in fields}


class PoCForm(forms.ModelForm):
    class Meta:
        model = PoC
        fields = ['image']

        widgets = {
            'image': forms.FileInput(attrs={'accept': ".jpg, .png, .jfif, .exif, .gif, .tiff, .bmp",
                                            'onchange': "add_poc_image($(this))"})
        }

        labels = {k: "" for k in fields}


POCFormSet = inlineformset_factory(Issues, PoC, form=PoCForm, extra=1, can_delete=True)


class UploadReport(forms.Form):
    # type = forms.CharField(max_length=100, choices=[("Nessus", "Nessus"), ("Rapid7", "Rapid7")])
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.csv'}))
