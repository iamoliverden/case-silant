from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('search/', views.search, name='search'),
    path('search_ent/', views.search_ent, name='search_ent'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logged_in/', views.landing_page_logged_in, name='landing_page_logged_in'),
    path('detailed_info_unauth/', views.detailed_info_unauth, name='detailed_info_unauth'),
    path('detailed_info_auth/', views.detailed_info_auth, name='detailed_info_auth'),
    path('technical_maintenance/', views.technical_maintenance, name='technical_maintenance'),
    path('claims/', ClaimListView.as_view(), name='claims'),
    path('claims_detailed/<int:pk>/', ClaimDetailView.as_view(), name='claims_detailed'),
    path('create_service_record/', TechnicalMaintenanceCreateView.as_view(), name='create_service_record'),
    path('edit_service_record/<int:pk>/', TechnicalMaintenanceUpdateView.as_view(), name='edit_service_record'),
    path('create_claim/', ClaimCreateView.as_view(), name='create_claim'),
    path('edit_claim/<int:pk>/', ClaimUpdateView.as_view(), name='edit_claim'),
]