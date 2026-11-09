from django.urls import path
from . import views

app_name = 'dfd_app'

urlpatterns = [
    # Pages
    path('', views.studio_view, name='studio'),
    path('templates/', views.templates_view, name='templates'),
    path('forensics/', views.forensics_view, name='forensics'),
    path('docs/', views.docs_view, name='docs'),

    # REST APIs
    path('api/validate/', views.api_validate, name='api_validate'),
    path('api/generate/', views.api_generate, name='api_generate'),
    path('api/autolayout/', views.api_autolayout, name='api_autolayout'),
    path('api/data-dictionary/', views.api_data_dictionary, name='api_data_dictionary'),
    path('api/projects/save/', views.api_save_project, name='api_save_project'),
    path('api/projects/<uuid:project_id>/', views.api_load_project, name='api_load_project'),
    path('api/forensics/scan/', views.api_forensic_scan, name='api_forensic_scan'),
]

