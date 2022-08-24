from django.urls import path
from . import views

urlpatterns = [
    path('', views.CaseListView.as_view(), name='cases'),
    path('cases/new/', views.CaseCreateView.as_view(), name='case-create'),
    path('cases/<int:pk>/update/', views.CaseUpdateView.as_view(), name='case-update'),
    path('recon/<int:pk>', views.recon, name='recon'),
    path('analysis/<int:pk>/', views.IssueListView.as_view(), name='analysis'),
    path('analysis/<int:case_pk>/issue/new', views.IssueCreateView.as_view(), name='issue-create'),
    path('analysis/<int:case_pk>/issue/<int:pk>/update', views.IssueUpdateView.as_view(), name='issue-update'),
    # path('analysis', views.analysis, name='analysis'),
    path('search_vulns', views.search_vulns, name='search_vulns'),
    path('get_recon_tools/<int:pk>', views.get_recon_tools, name='get_recon_tools'),
    path('get_issue_data/<int:pk>', views.get_issue_data, name='get_issue_data'),
    path('generateReport/<int:pk>', views.generateReport, name='generateReport'),
]
