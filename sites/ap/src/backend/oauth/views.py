from django.conf import settings
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginView(LoginView):

    authentication_form = AuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            login_redirect_url = getattr(settings, "LOGIN_REDIRECT_URL", "/")
            return redirect(login_redirect_url)

        return super().dispatch(request, *args, **kwargs)