from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, RedirectView


class HomePageView(TemplateView):
    """
    A home page view that with some customisable features.
    """
    template_name = "wagtail_client/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["settings"] = settings
        return context


@method_decorator(login_required, name="dispatch")
class ProtectedPageView(PermissionRequiredMixin, TemplateView):
    """
    A protected page view that with some customisable features.
    """
    template_name = "wagtail_client/protected.html"
    permission_required = 'polls.can_vote'

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
