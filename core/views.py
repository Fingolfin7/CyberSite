from datetime import datetime
import json
import tempfile
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from .models import Cases
from .forms import CaseForm, ReconForm, IssueFormSet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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


@login_required
def cases(request):
    if 'caseID' in request.session:
        del request.session['caseID']
    context = {
        "title": "Cases",
        "cases": Cases.objects.order_by('-lastUpdate')
    }
    return render(request, "core/Cases.html", context)


@login_required
def new_case(request, caseID=None):
    if request.method == "POST":
        if caseID:
            thisCase = Cases.objects.get(id=caseID)
            case = CaseForm(request.POST, request.FILES, instance=thisCase)
        else:
            case = CaseForm(request.POST, request.FILES)
        if case.is_valid():
            if case.has_changed():
                case.save()
            name = case.cleaned_data.get('caseName')
            request.session['caseID'] = Cases.objects.filter(caseName=name)[0].id
            return redirect('recon')
    else:
        if caseID:
            thisCase = Cases.objects.get(id=caseID)
            case = CaseForm(instance=thisCase)
            title = thisCase.caseName
        elif 'caseID' in request.session:
            thisCase = Cases.objects.get(id=request.session['caseID'])
            case = CaseForm(instance=thisCase)
            title = thisCase.caseName
        else:
            case = CaseForm()
            title = "New Case"

    context = {
        "title": title,
        "form": case
    }
    return render(request, 'core/NewCase.html', context)


def get_recon_tools(request):
    caseID = request.session['caseID']
    recon_tools = json.loads(Cases.objects.get(id=caseID).recon.tools)
    data = {
        'tools': recon_tools
    }
    return JsonResponse(data)


@login_required
def recon(request):
    caseID = request.session['caseID']

    if request.method == "POST":
        reconInstance = Cases.objects.get(id=caseID).recon
        recon_form = ReconForm(request.POST, instance=reconInstance)

        if recon_form.is_valid():
            recon_form.save()
            return redirect('analysis')
        else:
            for field in ['tools', 'passive_sources']:
                if field in recon_form.errors:
                    error = repr(recon_form.errors[field]).split('\'')[1]
                    messages.error(request, f"{field}: {error}")
    else:
        reconInstance = Cases.objects.get(id=caseID).recon
        recon_form = ReconForm(instance=reconInstance)

    context = {
        "title": "Reconnaissance",
        "form": recon_form
    }
    return render(request, 'core/Reconnaissance.html', context)


'''@login_required
def scan(request):
    if request.method == "POST":
        # do stuff
        return redirect('analysis')

    context = {
        "title": "Scan and Enumeration"
    }
    return render(request, 'core/Scan.html', context)'''


def get_issue_data(request):
    caseID = request.session['caseID']
    severity_totals = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0,
        "Info": 0,
    }

    issues = Cases.objects.get(id=caseID).issues_set.all()

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
            if request.POST['save'] == '1':
                messages.success(request, "Saved Successfully")
                return redirect('analysis')
            elif request.POST['save'] == '2':
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


@login_required
def generateReport(request):
    case = Cases.objects.get(id=request.session['caseID'])
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
