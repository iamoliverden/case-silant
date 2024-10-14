# list_views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from silant_app.filters.filters import GeneralInformationFilter, ClaimFilter, TechnicalMaintenanceFilter
from silant_app.models import Machine, Claim, TechnicalMaintenance
from silant_app.views.views_permissions import GeneralInformationPermissions, ClaimPermissions, MaintenancePermissions, GroupFourPermission

# General Information List View
class GeneralInformationListView(LoginRequiredMixin, GeneralInformationPermissions, ListView):
    model = Machine
    template_name = 'landing_page_ent.html'
    context_object_name = 'search_results'
    filterset_class = GeneralInformationFilter

    def get_queryset(self):
        user = self.request.user
        user_groups = user.groups.values_list('id', flat=True)

        if 4 in user_groups:
            machine_ids = Machine.objects.filter(client=user).values_list('id', flat=True)
            queryset = GeneralInformationFilter.objects.filter(machine__id__in=machine_ids)
        else:
            queryset = Machine.objects.all()

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset, user=user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['user_name'] = self.request.user.username
        context['is_manager'] = self.request.user.groups.filter(id=1).exists()
        return context


# Claim List View
class ClaimListView(LoginRequiredMixin, ClaimPermissions, ListView):
    model = Claim
    template_name = 'claims.html'
    context_object_name = 'claims'
    filterset_class = ClaimFilter

    def get_queryset(self):
        user = self.request.user
        user_groups = user.groups.values_list('id', flat=True)

        if 4 in user_groups:
            machine_ids = Machine.objects.filter(client=user).values_list('id', flat=True)
            queryset = Claim.objects.filter(machine__id__in=machine_ids)
        else:
            queryset = Claim.objects.all()

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset, user=user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['user_name'] = self.request.user.username
        context['can_edit_or_add'] = self.can_edit_or_add()
        return context

    def can_edit_or_add(self):
        user_groups = self.request.user.groups.values_list('id', flat=True)
        return any(group_id in [1, 3, 5] for group_id in user_groups)


# Technical Maintenance List View
class TechnicalMaintenanceListView(LoginRequiredMixin, MaintenancePermissions, GroupFourPermission, ListView):
    model = TechnicalMaintenance
    template_name = 'technical_maintenance.html'
    context_object_name = 'maintenances_records'
    filterset_class = TechnicalMaintenanceFilter

    def get_queryset(self):
        user = self.request.user
        user_groups = user.groups.values_list('id', flat=True)

        if 4 in user_groups:
            machine_ids = Machine.objects.filter(client=user).values_list('id', flat=True)
            queryset = TechnicalMaintenance.objects.filter(machine__id__in=machine_ids)
        else:
            queryset = TechnicalMaintenance.objects.all()

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset, user=user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        serial_number = self.request.GET.get('serial_number')
        machine = Machine.objects.filter(serial_number=serial_number).first()
        context['filter'] = self.filterset
        context['user_name'] = self.request.user.username
        context['machine'] = machine
        context['can_edit_or_add'] = self.can_edit_or_add()
        return context

    def can_edit_or_add(self):
        user_groups = self.request.user.groups.values_list('id', flat=True)
        return any(group_id in [1, 3, 5] for group_id in user_groups)


