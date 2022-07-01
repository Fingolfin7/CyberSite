import json
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Cases, Issues, Recon
from .forms import CaseForm, ReconForm, IssueFormSet
from django.contrib import messages



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
            case.save()
            name = case.cleaned_data.get('caseName')
            request.session['caseID'] = Cases.objects.filter(caseName=name)[0].id
            return redirect('recon')
    else:
        if caseID:
            thisCase = Cases.objects.get(id=caseID)
            case = CaseForm(instance=thisCase)
        elif not caseID and 'caseID' in request.session:
            thisCase = Cases.objects.get(id=request.session['caseID'])
            case = CaseForm(instance=thisCase)
        else:
            case = CaseForm()

    context = {
        "title": "New Case",
        "form": case
    }
    return render(request, 'core/NewCase.html', context)


@login_required
def recon(request):
    caseID = request.session['caseID']

    if request.method == "POST":
        reconInstance = Cases.objects.get(id=caseID).recon
        recon_form = ReconForm(request.POST, instance=reconInstance)

        if recon_form.is_valid():
            recon_form.save()
            return redirect('scan')
        else:
            for field in ['tools', 'passive_sources']:
                if field in recon_form.errors:
                    error = repr(recon_form.errors[field]).split('\'')[1]
                    messages.error(request, f"{field}: {error}")
    else:
        reconInstance = Cases.objects.get(id=caseID).recon
        # tools_dict = json.loads(reconInstance.tools)
        recon_form = ReconForm(instance=reconInstance)
        if recon_form.is_valid():
            recon_form.save()
            return redirect('scan')

    # if len(tools_dict) == 0:
    #   tools_dict = None

    context = {
        "title": "Reconnaissance",
        "form": recon_form
        # "toolsDict": tools_dict
    }
    return render(request, 'core/Reconnaissance.html', context)


@login_required
def scan(request):
    if request.method == "POST":
        # do stuff
        return redirect('analysis')

    context = {
        "title": "Scan and Enumeration"
    }
    return render(request, 'core/Scan.html', context)


@login_required
def analysis(request):
    if request.method == "POST":
        # do stuff
        return redirect('')

    context = {
        "title": "Analysis",
    }
    return render(request, 'core/Analysis.html', context)


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
