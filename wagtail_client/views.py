from django.conf import settings
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """
    A home page view that with some customisable features.
    """
    template_name = "wagtail_client/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["site_name"] = settings.WAGTAIL_SITE_NAME
        context["site_colour"] = settings.WAGTAIL_SITE_COLOUR
        context["redirect_url"] = settings.WAGTAIL_REDIRECT_URL
        return context
