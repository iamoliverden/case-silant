from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('search/', views.search, name='search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('loggedin/', views.landing_page_loggedin, name='landing_page_loggedin'),
    path('search_loggedin/', views.search_loggedin, name='search_loggedin'),
    path('general_info/', views.general_info, name='general_info'),
    path('technical_maintenance/', views.technical_maintenance, name='technical_maintenance'),
    path('claims/', views.claims, name='claims'),
]