from django.urls import path
from . import views

urlpatterns = [
    path('', views.cases, name='cases'),
    path('new_case/', views.new_case, name='new_case'),
    path('new_case/<caseID>', views.new_case, name='new_case'),
    path('recon', views.recon, name='recon'),
    path('scan', views.scan, name='scan'),
    path('analysis', views.analysis, name='analysis'),
    path('test_page', views.test_page, name='test_page'),
]
