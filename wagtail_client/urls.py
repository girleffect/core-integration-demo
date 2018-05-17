"""wagtail_client URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from wagtail_client.views import (
    HomePageView,
    ProtectedPageView,
    LoginRedirectWithQueryStringView,
    RedirectRegister
)


urlpatterns = [
    # Override default Django admin login
    url(r'^admin/login/', LoginRedirectWithQueryStringView.as_view()),
    url(r'^admin/', admin.site.urls),
    # Override default Wagtail admin login
    url(r'^cms/login/', LoginRedirectWithQueryStringView.as_view()),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^pages/', include(wagtail_urls)),
    url(r'^oidc/', include('mozilla_django_oidc.urls')),
    url(r'^protected/', ProtectedPageView.as_view(), name="protected"),
    url(r'^login/', LoginRedirectWithQueryStringView.as_view(), name="login"),
    url(r"^$", HomePageView.as_view(), name="home"),
    url(
        r"^register-redirect/$",
        RedirectRegister.as_view(),
        name="register_redirect"
    )
]
