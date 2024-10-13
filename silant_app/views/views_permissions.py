from django.contrib.auth.mixins import UserPassesTestMixin
from silant_app.models import TechnicalMaintenance, Claim

class MaintenanceRecordPermissions(UserPassesTestMixin):
    def test_func(self):
        user_groups = self.request.user.groups.values_list('name', flat=True)
        return any(group in ['Service Companies', 'Managers', 'Admins', 'Clients'] for group in user_groups)



class MaintenancePermissions(UserPassesTestMixin):
    def test_func(self):
        user_groups = self.request.user.groups.values_list('id', flat=True)
        return any(group_id in [1, 3, 4, 5] for group_id in user_groups)


class GeneralInformationPermissions(UserPassesTestMixin):
    def test_func(self):
        user_groups = self.request.user.groups.values_list('id', flat=True)
        return any(group_id in [1, 3, 5] for group_id in user_groups)


class ClaimPermissions(UserPassesTestMixin):
    def test_func(self):
        user_groups = self.request.user.groups.values_list('id', flat=True)
        return any(group_id in [1, 3, 4, 5] for group_id in user_groups)


class MachinePermissions(UserPassesTestMixin):
    def test_func(self):
        user_groups = self.request.user.groups.values_list('id', flat=True)
        return any(group_id in [1] for group_id in user_groups)


class GroupFourPermission(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        user_groups = user.groups.values_list('id', flat=True)

        # Check if the user is in group 4
        if 4 in user_groups:
            # Determine if the record pertains to their machine
            try:
                obj = self.get_object()
                if isinstance(obj, Claim):
                    return obj.machine.client == user
                elif isinstance(obj, TechnicalMaintenance):
                    return obj.machine.client == user
            except AttributeError:
                return False
        return True
