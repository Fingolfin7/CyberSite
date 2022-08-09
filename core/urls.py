from django.urls import path
from . import views

urlpatterns = [
    path('', views.CaseListView.as_view(), name='cases'),
    path('cases/new/', views.CaseCreateView.as_view(), name='case-create'),
    path('cases/<int:pk>/update/', views.CaseUpdateView.as_view(), name='case-update'),
    path('recon/<int:pk>', views.recon, name='recon'),
    # path('scan', views.scan, name='scan'),
    path('analysis', views.analysis, name='analysis'),
    path('test_page', views.test_page, name='test_page'),
    path('search_vulns', views.search_vulns, name='search_vulns'),
    path('get_recon_tools/<int:pk>', views.get_recon_tools, name='get_recon_tools'),
    path('get_issue_data', views.get_issue_data, name='get_issue_data'),
    path('generateReport', views.generateReport, name='generateReport'),
]
