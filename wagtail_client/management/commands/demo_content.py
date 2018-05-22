# NOTE: Management command only to be used for setting up demo environments, do
# not use for anything else.
import os

from django.contrib.sites.models import Site
from django.core.management import BaseCommand

from wagtail_client.models import OidcSettings


class Command(BaseCommand):
    help = "Setup used for demonstration purposes only"

    def handle(self, *args, **options):
        site_code = os.getenv("SITE_CODE")
        self.stdout.write(self.style.SUCCESS("Creating sites..."))
        if site_code == "springster":
            site, created = Site.objects.update_or_create(
                id=1, defaults={
                    "domain": "wagtail-demo-1-site-1",
                    "name": "Wagtail Demo 1 Site 1",
                }
            )
            self.stdout.write(self.style.SUCCESS("{} {}".format("Created" if created else
                                                                "Updated", site)))
            oidcsettings, created = OidcSettings.objects.update_or_create(
                site=site, defaults={
                    "oidc_rp_client_id": "client_id_1",
                    "oidc_rp_client_secret": "super_client_secret_1",
                    "oidc_rp_scopes": "openid profile email address phone site roles",
                    "extra_params": {"theme": "springster"},
                    "wagtail_redirect_url": "http://wagtail-demo-1-site-1:8000/"
                }
            )
            self.stdout.write(self.style.SUCCESS("{} {}".format("Created" if created else
                                                                "Updated", oidcsettings)))

            site, created = Site.objects.update_or_create(
                id=2, defaults={
                    "domain": "wagtail-demo-1-site-2",
                    "name": "Wagtail Demo 1 Site 2",

                }
            )
            self.stdout.write(self.style.SUCCESS("{} {}".format("Created" if created else
                                                                "Updated", site)))
            oidcsettings, created = OidcSettings.objects.update_or_create(
                site=site, defaults={
                    "oidc_rp_client_id": "client_id_3",
                    "oidc_rp_client_secret": "super_client_secret_3",
                    "oidc_rp_scopes": "openid profile email address phone site roles",
                    "extra_params": {"theme": "springster"},
                    "wagtail_redirect_url": "http://wagtail-demo-1-site-2:8000/"
                }
            )
            self.stdout.write(self.style.SUCCESS("{} {}".format("Created" if created else
                                                                "Updated", oidcsettings)))

        elif site_code == "ninyampinga":
            site, created = Site.objects.update_or_create(
                id=1, defaults={
                    "domain": "wagtail-demo-2-site-1",
                    "name": "Wagtail Demo 2 Site 1",
                }
            )
            self.stdout.write(self.style.SUCCESS("{} {}".format("Created" if created else
                                                                "Updated", site)))
            oidcsettings, created = OidcSettings.objects.update_or_create(
                site=site, defaults={
                    "oidc_rp_client_id": "client_id_2",
                    "oidc_rp_client_secret": "super_client_secret_2",
                    "oidc_rp_scopes": "openid profile email address phone site roles",
                    "extra_params": {"theme": "ninyampinga"},
                    "wagtail_redirect_url": "http://wagtail-demo-2-site-1:8000/"
                }
            )
            self.stdout.write(self.style.SUCCESS("{} {}".format("Created" if created else
                                                                "Updated", oidcsettings)))
        else:
            self.stdout.write(self.style.SUCCESS(f"Nothing to do for {site_code}"))

