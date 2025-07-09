from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

# Helper functions
def is_in_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

# Admin required
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if is_in_group(request.user, 'Admin'):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

# Organizer required
def organizer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if is_in_group(request.user, 'Organizer'):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

# Participant required
def participant_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if is_in_group(request.user, 'Participant'):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view
