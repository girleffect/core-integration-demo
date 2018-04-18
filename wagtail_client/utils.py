from django.conf import settings


def provider_logout_url(request):
    """
    This function is used to construct a logout URL that can be used to log the user out of
    the Identity Provider (Authentication Service).
    :param request:
    :return:
    """
    # TODO: The current implementation will only work as long as you are logging out of the last
    # site you logged in to. If you logged into another site after the one you are logging out from
    # now, you will be redirected there.
    redirect_url = settings.OIDC_OP_LOGOUT_URL + "?next=/redirect/"
    return redirect_url
