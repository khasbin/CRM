from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from leads.models import User

class OrganizerorLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated or is an organizer."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organizer:
            return redirect("leads:lead-list")
        return super().dispatch(request, *args, **kwargs)


