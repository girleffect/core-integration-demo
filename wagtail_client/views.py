from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView,
    RedirectView
)
from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCAuthenticationCallbackView


class HomePageView(TemplateView):
    """
    A home page view that with some customisable features.
    """
    template_name = "wagtail_client/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["settings"] = settings
        context["site"] = get_current_site(self.request)
        return context


@method_decorator(login_required, name="dispatch")
class ProtectedPageView(TemplateView):
    """
    A protected page view that with some customisable features.
    """
    template_name = "wagtail_client/protected.html"

    def get_context_data(self, **kwargs):
        context = super(ProtectedPageView, self).get_context_data(**kwargs)
        context["settings"] = settings
        return context


class LoginRedirectWithQueryStringView(RedirectView):
    """
    This view is used when a user needs to be redirected to the Authentication Service
    for login. The problem is that this view is also used when a user is already logged
    in but does not have the required permissions to view a resource.

    This view specifically checks if a user is already logged in, in which case it redirects
    the user to the homepage with a message explaining that access to the resource that was
    accessed is not allowed.
    """
    query_string = True
    pattern_name = "oidc_authentication_init"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # Since the user is already logged in, we take them to the home page.
            messages.info(self.request, "You are already logged in, but may not have the "
                                        "required permissions.")
            return redirect(reverse("home"))

        return super().dispatch(request, *args, **kwargs)


class RedirectRegister(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        # Reverses or reverse_lazy in urls.py caused circular imports. Seemingly.
        return reverse("oidc_authentication_init") + f"?next={reverse('home')}"


class CustomAuthenticationRequestView(OIDCAuthenticationRequestView):
    """
    To support multi-site setups, we need to replace cases where the
    Mozilla OIDC Client references any of the following:
    * settings.OIDC_RP_CLIENT_ID
    * settings.OIDC_RP_CLIENT_SECRET
    * settings.OIDC_RP_SCOPES
    * settings.WAGTAIL_REDIRECT_URL

    These are typically referenced in the constructors of most classes,
    but we have to make sure it is proper on the functions where we have
    a request (since we can get the current site from the request).
    """

    def get(self, request):
        """
        In order to support proper login handling for multi-site configurations,
        we need to set the applicable CLIENT_ID and CLIENT_SECRET.
        :param request:
        :return:
        """
        site = get_current_site(request)
        if not hasattr(site, "oidcsettings"):
            raise RuntimeError(f"Site {site} has no settings configured.")

        self.OIDC_RP_CLIENT_ID = site.oidcsettings.oidc_rp_client_id
        self.OIDC_RP_SCOPES = site.oidcsettings.oidc_rp_scopes
        return super().get(request)

    def get_extra_params(self, request):
        """
        Extra parameters can be passed along in the login URL that is
        generated. Set these parameters here.
        """
        params = super().get_extra_params(request)
        site = get_current_site(request)
        if not hasattr(site, "oidcsettings"):
            raise RuntimeError(f"Site {site} has no settings configured.")

        params.update(site.oidcsettings.extra_params)
        return params


class CustomAuthenticationCallbackView(OIDCAuthenticationCallbackView):
    """
    To support multi-site setups, we need to replace cases where the
    Mozilla OIDC Client references any of the following:
    * settings.OIDC_RP_CLIENT_ID
    * settings.OIDC_RP_CLIENT_SECRET
    * settings.OIDC_RP_SCOPES ??
    * settings.LOGIN_REDIRECT_URL

    These are typically referenced in the constructors of most classes,
    but we have to make sure it is proper on the functions where we have
    a request (since we can get the current site from the request).
    """
    @property
    def failure_url(self):
        """
        The URL to redirect to for a login failure can be customised here.
        The request is available in self.request.
        """
        return super().failure_url

    @property
    def success_url(self):
        """
        The URL to redirect to for a successful login can be customised here.
        The request is available in self.request.
        """
        return super().success_url
