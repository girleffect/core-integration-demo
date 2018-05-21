from django.contrib.postgres.fields import JSONField
from django.db import models


class OidcSettings(models.Model):
    site = models.OneToOneField("sites.Site")
    oidc_rp_client_id = models.CharField(max_length=255)
    oidc_rp_client_secret = models.CharField(max_length=255)
    oidc_rp_scopes = models.CharField(blank=True, max_length=255,
                                      default='openid profile email address phone site roles')
    extra_params = JSONField(blank=True, default={})
    wagtail_redirect_url = models.URLField()

    def __str__(self):
        return f"{self.site} {self.oidc_rp_client_id}"
