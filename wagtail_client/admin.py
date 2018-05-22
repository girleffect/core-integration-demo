from django.contrib import admin

from wagtail_client import models


class OidcSettingsAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = "OIDC Settings"


admin.site.register(models.OidcSettings, OidcSettingsAdmin)
