# urls.py

from django.urls import path
from silant_app.views.views import *
from silant_app.views.create_views import *
from silant_app.views.detail_views import *
from silant_app.views.list_views import *
from silant_app.views.update_views import *


urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('search/', search, name='search'),
    path('search_ent/', GeneralInformationListView.as_view(), name='search_ent'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('logged_in/', landing_page_logged_in, name='landing_page_logged_in'),
    path('detailed_info_unauth/', detailed_info_unauth, name='detailed_info_unauth'),
    path('detailed_info_auth/', detailed_info_auth, name='detailed_info_auth'),
    path('technical_maintenance/', TechnicalMaintenanceListView.as_view(), name='technical_maintenance'),
    path('claims/', ClaimListView.as_view(), name='claims'),
    path('claims_detailed/<int:pk>/', ClaimDetailView.as_view(), name='claims_detailed'),
    path('create_service_record/', TechnicalMaintenanceCreateView.as_view(), name='create_service_record'),
    path('edit_service_record/<int:pk>/', TechnicalMaintenanceUpdateView.as_view(), name='edit_service_record'),
    path('create_claim/', ClaimCreateView.as_view(), name='create_claim'),
    path('edit_claim/<int:pk>/', ClaimUpdateView.as_view(), name='edit_claim'),
    path('create_machine/', MachineCreateView.as_view(), name='create_machine'),
    path('edit_machine/<int:pk>/', MachineUpdateView.as_view(), name='edit-machine'),

]