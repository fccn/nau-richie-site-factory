"""Custom login view implementation"""

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


# pylint: disable=too-many-ancestors
class CustomLoginView(LoginView):
    """Custom `LoginView` implementation to override `dispatch`"""

    authentication_form = AuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        """
        Try to dispatch to the right method; if a method doesn't exist,
        defer to the error handler. Also defer to the error handler if the
        request method isn't on the approved list.
        """

        if request.user.is_authenticated:
            login_redirect_url = getattr(settings, "LOGIN_REDIRECT_URL", "/")
            return redirect(login_redirect_url)

        return super().dispatch(request, *args, **kwargs)
