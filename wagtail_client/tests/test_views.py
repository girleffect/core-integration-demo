from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


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

    def test_homepage_auth_logic(self):
        response = self.client.get(
            reverse("home")
        )
        self.assertNotContains(response, self.user.email)
        self.client.login(username=self.user.username, password="L1lly")
        response = self.client.get(
            reverse("home")
        )
        self.assertContains(response, self.user.email)
