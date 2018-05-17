from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView,
    RedirectView
)


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
class ProtectedPageView(TemplateView):
    """
    A protected page view that with some customisable features.
    """
    template_name = "wagtail_client/protected.html"

    def get_context_data(self, **kwargs):
        context = super(ProtectedPageView, self).get_context_data(**kwargs)
        context["settings"] = settings
        return context


class RedirectWithQueryStringView(RedirectView):
    query_string = True


class RedirectRegister(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        # Reverses or reverse_lazy in urls.py caused circular imports. Seemingly.
        return reverse("oidc_authentication_init") + f"?next={reverse('home')}"
