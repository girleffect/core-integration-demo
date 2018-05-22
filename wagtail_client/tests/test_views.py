from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase

from wagtail_client.models import OidcSettings


class TestOIDCSessionMiddleware(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TestOIDCSessionMiddleware, cls).setUpTestData()
        cls.user = get_user_model().objects.create(
            username="Poppy",
            email="poppy@hammerkeeper.com"
        )
        cls.user.set_password("L1lly")
        cls.user.save()

        cls.site = Site.objects.get(name="example.com")
        oidc_settings, created = OidcSettings.objects.update_or_create(
            site=cls.site, defaults={
                "oidc_rp_client_id": "foo",
                "oidc_rp_client_secret": "bar",
                "wagtail_redirect_url": "http://localhost/",
                "oidc_rp_scopes": "openid profile email address phone site roles"
            })

    def test_homepage_auth_logic(self):
        response = self.client.get(
            reverse("home")
        )
        self.assertNotContains(response, self.user.email)
        self.client.login(username=self.user.username, password="L1lly")
        response = self.client.get(
            reverse("home")
        )
        self.assertContains(response, self.site.name)
