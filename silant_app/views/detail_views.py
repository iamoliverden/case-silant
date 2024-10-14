# detailed_view.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from silant_app.models import Machine, Claim
from silant_app.views.views_permissions import ClaimPermissions, GroupFourPermission

from django.contrib.auth.mixins import LoginRequiredMixin


# Claim detail view (authenticated)
class ClaimDetailView(LoginRequiredMixin, ClaimPermissions, GroupFourPermission, DetailView):
    model = Claim
    template_name = 'claims_detailed.html'
    context_object_name = 'claim'

    def get_context_data(self, **kwargs):
        # Add the user's name to the context
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.request.user.username
        return context


# Detailed information view (unauthenticated)
def detailed_info_unauth(request):
    serial_number = request.GET.get('serial_number')
    machine = Machine.objects.filter(serial_number=serial_number).first()
    user_name = request.user.username
    return render(request, 'detailed_info_unauth.html', {'machine': machine, 'user_name': user_name})


# Detailed information view (authenticated)
@login_required
def detailed_info_auth(request):
    serial_number = request.GET.get('serial_number')
    machine = Machine.objects.filter(serial_number=serial_number).first()
    user_name = request.user.username
    return render(request, 'detailed_info_auth.html', {'machine': machine, 'user_name': user_name})
