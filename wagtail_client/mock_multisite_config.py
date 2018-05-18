from django.conf import settings


def get_config_for_site(site):
    """
    """
    return {
        "OIDC_RP_CLIENT_ID": settings.OIDC_RP_CLIENT_ID,
        "OIDC_RP_CLIENT_SECRET": settings.OIDC_RP_CLIENT_SECRET
    }