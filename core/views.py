from datetime import datetime
import json
import tempfile
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from .models import Cases, Issues
from .forms import CaseForm, ReconForm, IssueForm, IssueFormSet
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView


def search_vulns(request):
    search_val = request.GET.get('search_val', None)
    vuln_source = request.GET.get('vuln_source', None)

    with open(f'core/static/core/vulnerabilities/{vuln_source}', 'r', encoding='latin1') as reader:
        vulnerabilities = json.loads(reader.read())
    data = {
        'results': [i for i in vulnerabilities if
                    search_val.lower() in i['title'].lower() and search_val != ""]
    }
    return JsonResponse(data)


class CaseListView(ListView):
    model = Cases
    template_name = 'core/home.html'
    context_object_name = 'cases'
    ordering = ['-lastUpdate']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cases'
        return context


class CaseCreateView(LoginRequiredMixin, CreateView):
    model = Cases
    form_class = CaseForm
    template_name = 'core/cases.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recon')

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


@login_required
def analysis(request):
    case = Cases.objects.get(id=request.session['caseID'])
    orderIssues = case.issues_set.order_by("-id")
    if request.method == "POST":
        formset = IssueFormSet(request.POST, request.FILES, instance=case, queryset=orderIssues)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved Successfully")
            return redirect('analysis')
        else:
            messages.error(request, f"{formset.errors}{formset.non_form_errors()}")
    else:

        formset = IssueFormSet(instance=case, queryset=orderIssues)

    context = {
        "title": "Analysis",
        "formset": formset
    }
    return render(request, 'core/Analysis.html', context)


class IssueListView(LoginRequiredMixin, ListView):
    template_name = "core/issues_list.html"
    context_object_name = "issues"

    def get_queryset(self):
        return Cases.objects.get(id=self.kwargs['pk']).issues_set.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Analysis"
        return context


class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issues
    form_class = IssueForm
    template_name = 'core/issue.html'

    def form_valid(self, form):
        form.instance.case = Cases.objects.get(id=self.kwargs['case_pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Issue"
        return context


class IssueUpdateView(LoginRequiredMixin, UpdateView):
    model = Issues
    form_class = IssueForm
    template_name = 'core/issue.html'

    def form_valid(self, form):
        messages.success(self.request, "Saved Successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Issue"
        return context


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
                'name': issue.name,
                'severity': issue.severity,
                'affected_hosts': issue.affected_hosts,
                'description': issue.description,
                'impact': issue.impact,
                'solution': issue.solution,
                'reference': issue.reference,
                'cvss_rating': issue.cvss_rating,
                'proof_screenshot': InlineImage(doc, image_descriptor=issue.proof_screenshot, width=Cm(10))
                if issue.proof_screenshot
                else '',
            } for issue in case.issues_set.all()
        ],
        'issues_count': len(case.issues_set.all())
    }

    doc.render(context)
    doc.save(tmp.name)
    stream_file = open(tmp.name, 'rb')
    return FileResponse(stream_file, as_attachment=True, filename=f'{case.caseName} Report.docx')


@login_required
def test_page(request):
    case = Cases.objects.get(id=request.session['caseID'])
    orderIssues = case.issues_set.order_by("-id")
    if request.method == "POST":
        formset = IssueFormSet(request.POST, request.FILES, instance=case, queryset=orderIssues)
        if formset.is_valid():
            formset.save()
            return redirect('test_page')
    else:
        # messages.error(request, f"{formset.errors}{formset.non_form_errors()}")
        formset = IssueFormSet(instance=case, queryset=orderIssues)

    context = {
        "title": "Test",
        "formset": formset
    }
    return render(request, 'core/test_template.html', context)
