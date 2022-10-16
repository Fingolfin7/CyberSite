from datetime import datetime
import json
import tempfile
from django.db import transaction
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from .models import Cases, Issues, PoC
from vulnerabilities.models import *
from .forms import CaseForm, ReconForm, IssueForm, POCFormSet
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from cleantext import clean


def search_vulns(request):
    search_val = request.GET.get('search_val', None)
    vuln_source = int(request.GET.get('vuln_source', None))

    vulnList = [VulnerabilitiesGeneral, VulnerabilitiesCWE, VulnerabilitiesOWASP,
                VulnerabilitiesMobile, VulnerabilitiesEnterprise]

    vulnerabilities = vulnList[vuln_source].objects.filter(title__contains=search_val.lower()).values()
    vulnerabilities = list(vulnerabilities)

    data = {
        'results': vulnerabilities
    }

    return JsonResponse(data)


class CaseListView(ListView):
    model = Cases
    template_name = 'core/home.html'
    context_object_name = 'cases'
    ordering = ['-lastUpdate']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cases'
        return context


class CaseCreateView(LoginRequiredMixin, CreateView):
    model = Cases
    form_class = CaseForm
    template_name = 'core/cases.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Case'
        return context


class CaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Cases
    form_class = CaseForm
    template_name = 'core/cases.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().caseName
        return context


class CaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Cases
    context_object_name = 'case'
    template_name = 'core/delete_case.html'
    # success_url = '/'
    success_message = 'Case Deleted'

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return super(CaseDeleteView, self).delete(request, *args, **kwargs)


def get_recon_tools(request, pk: int):
    recon_tools = json.loads(Cases.objects.get(id=pk).recon.tools)
    data = {
        'tools': recon_tools
    }
    return JsonResponse(data)


@login_required
def recon(request, pk: int):
    if request.method == "POST":
        reconInstance = Cases.objects.get(id=pk).recon
        recon_form = ReconForm(request.POST, instance=reconInstance)

        if recon_form.is_valid():
            recon_form.save()
            if recon_form.has_changed():
                reconInstance.case.save()  # update last saved date for case by saving the case
            return redirect('analysis', pk)
        else:
            for field in ['tools', 'passive_sources']:
                if field in recon_form.errors:
                    error = repr(recon_form.errors[field]).split('\'')[1]
                    messages.error(request, f"{field}: {error}")
    else:
        reconInstance = Cases.objects.get(id=pk).recon
        recon_form = ReconForm(instance=reconInstance)

    context = {
        "title": "Reconnaissance",
        "form": recon_form
    }
    return render(request, 'core/Reconnaissance.html', context)


def get_issue_data(request, pk: int):
    severity_totals = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0,
        "Info": 0,
    }

    issues = Cases.objects.get(id=pk).issues_set.all()

    for issue in issues:
        if issue.severity in severity_totals:
            severity_totals[issue.severity] += 1

    data = {
        'severity_totals': severity_totals
    }
    return JsonResponse(data)


class IssueListView(LoginRequiredMixin, ListView):
    template_name = "core/issues_list.html"
    context_object_name = "issues"
    paginate_by = 7

    def get_queryset(self):
        return Cases.objects.get(id=self.kwargs['pk']).issues_set.order_by("-lastUpdate")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Analysis"
        context['case_id'] = self.kwargs['pk']
        return context


class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issues
    form_class = IssueForm
    template_name = 'core/issue_create.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        case = Cases.objects.get(id=self.kwargs['case_pk'])
        form.instance.case = case
        if form.is_valid():
            issueInstance = form.save()
            case.save()  # update last saved date for case by saving the case
            poc_images = POCFormSet(self.request.POST, self.request.FILES)
            if poc_images.is_valid():
                poc_images.instance = issueInstance
                poc_images.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('analysis', kwargs={'pk': self.kwargs['case_pk']})

    def get_context_data(self, **kwargs):
        context = super(IssueCreateView, self).get_context_data(**kwargs)
        context['poc_images'] = POCFormSet()
        context['title'] = "New Issue"
        context['case_id'] = self.kwargs['case_pk']
        return context


class IssueUpdateView(LoginRequiredMixin, UpdateView):
    model = Issues
    form_class = IssueForm
    template_name = 'core/issue_update.html'

    def form_valid(self, form):
        context = self.get_context_data()
        case = Cases.objects.get(id=self.kwargs['case_pk'])
        form.instance.case = case
        case.save()  # update last saved date for case by saving the case
        poc_images = context['poc_images']

        if poc_images.is_valid():
            messages.success(self.request, "Saved Successfully")
            # poc_images.instance = self.object
            poc_images.save()
            return super().form_valid(form)

    def get_queryset(self):
        return Cases.objects.get(id=self.kwargs['case_pk']).issues_set.filter(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(IssueUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['poc_images'] = POCFormSet(self.request.POST, self.request.FILES,
                                               instance=self.object)
        else:
            context['poc_images'] = POCFormSet(instance=self.object)
        context['title'] = f'{self.object.case.caseName} - {self.object.name}'
        return context


class IssueDeleteView(LoginRequiredMixin, DeleteView):
    model = Issues
    template_name = "core/delete_issue.html"
    context_object_name = "issue"
    success_message = "Issue deleted"

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        Cases.objects.get(id=self.kwargs['case_pk']).save()  # update last saved date for case by saving the case
        return super(IssueDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('analysis', kwargs={'pk': self.kwargs['case_pk']})


@login_required
def Issues(request, *args, **kwargs):
    issueInstance = Cases.objects.get(id=kwargs['case_pk']).issues_set.get(id=kwargs['pk'])
    if request.method == "POST":
        form = IssueForm(request.POST, instance=issueInstance)
        poc = POCFormSet(request.POST, request.FILES, instance=issueInstance)

        if form.is_valid() and poc.is_valid():
            messages.success(request, "Saved Successfully")
            form.save()
            poc.save()
            return redirect('analysis', kwargs['case_pk'])
        else:
            messages.error(request, f"Form: {form.errors}" if form.errors else
            f"POC: {poc.errors}")

    else:
        form = IssueForm(instance=issueInstance)
        poc = POCFormSet(instance=issueInstance)

    context = {
        "title": "Reconnaissance",
        "form": form,
        "poc_images": poc
    }
    return render(request, 'core/issue.html', context)


@login_required
def generateReport(request, pk: int):
    case = Cases.objects.get(id=pk)
    tmp = tempfile.NamedTemporaryFile(delete=False)  # create a temporary file
    doc = DocxTemplate("core/static/core/report template/Report Template.docx")

    context = {
        'cover_date': datetime.now().strftime("%B %Y"),
        'date': datetime.now().strftime("%d %B %Y"),
        'case': {
            'caseName': case.caseName,
            'organization': case.organization,
            'caseLead': case.caseLead,
            'orgHandler': case.orgHandler,
            'assessmentType': case.assessmentType.replace(':', ''),
            'scope': case.scope,
            'logo': InlineImage(doc, image_descriptor=case.logo,
                                width=Cm(5)),
            'createDate': case.createDate.strftime("%B %d, %Y"),
            'lastUpdate': case.lastUpdate.strftime("%B %d, %Y")
        },
        'issues': [
            {
                'name': clean(issue.name, fix_unicode=True, to_ascii=True, lower=False),
                'severity': clean(issue.severity, fix_unicode=True, to_ascii=True, lower=False),
                'affected_hosts': clean(issue.affected_hosts, fix_unicode=True, to_ascii=True, lower=False),
                'description': clean(issue.description, fix_unicode=True, to_ascii=True, lower=False),
                'impact': clean(issue.impact, fix_unicode=True, to_ascii=True, lower=False),
                'solution': clean(issue.solution, fix_unicode=True, to_ascii=True, lower=False),
                'reference': issue.reference,
                'cvss_rating': issue.cvss_rating,
                'poc_list': [InlineImage(doc, image_descriptor=poc.image, width=Cm(10))
                             for poc in issue.poc_set.all()],
            } for issue in case.issues_set.all()
        ],
        'issues_count': len(case.issues_set.all())
    }

    doc.render(context)
    doc.save(tmp.name)
    stream_file = open(tmp.name, 'rb')
    return FileResponse(stream_file, as_attachment=True, filename=f'{case.caseName} Report.docx')
