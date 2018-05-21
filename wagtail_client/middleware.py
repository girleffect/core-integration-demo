import time
from urllib.parse import urlencode

from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from mozilla_django_oidc.middleware import SessionRefresh
from mozilla_django_oidc.utils import import_from_settings, absolutify


class CustomSessionRefresh(SessionRefresh):
    """
    Customised version of mozilla_django_oidc.middleware.SessionRefresh
    Allows for reading site-specific configuration based on the request.
    """

    def process_request(self, request):
        site = get_current_site(request)
        if not hasattr(site, "oidcsettings"):
            raise RuntimeError(f"Site {site} has no settings configured.")

        if not self.is_refreshable_url(request):
            return

        expiration = request.session.get('oidc_id_token_expiration', 0)
        now = time.time()
        if expiration > now:
            # The id_token is still valid, so we don't have to do anything.
            return

        # The id_token has expired, so we have to re-authenticate silently.
        auth_url = import_from_settings('OIDC_OP_AUTHORIZATION_ENDPOINT')
        client_id = site.oidcsettings.oidc_rp_client_id
        state = get_random_string(import_from_settings('OIDC_STATE_SIZE', 32))

        # Build the parameters as if we were doing a real auth handoff, except
        # we also include prompt=none.
        params = {
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': absolutify(
                request,
                reverse('oidc_authentication_callback')
            ),
            'state': state,
            'scope': site.oidcsettings.oidc_rp_scopes,
            'prompt': 'none',
        }

        if import_from_settings('OIDC_USE_NONCE', True):
            nonce = get_random_string(import_from_settings('OIDC_NONCE_SIZE', 32))
            params.update({
                'nonce': nonce
            })
            request.session['oidc_nonce'] = nonce

        request.session['oidc_state'] = state
        request.session['oidc_login_next'] = request.get_full_path()

        query = urlencode(params)
        redirect_url = '{url}?{query}'.format(url=auth_url, query=query)
        if request.is_ajax():
            # Almost all XHR request handling in client-side code struggles
            # with redirects since redirecting to a page where the user
            # is supposed to do something is extremely unlikely to work
            # in an XHR request. Make a special response for these kinds
            # of requests.
            # The use of 403 Forbidden is to match the fact that this
            # middleware doesn't really want the user in if they don't
            # refresh their session.
            response = JsonResponse({'refresh_url': redirect_url}, status=403)
            response['refresh_url'] = redirect_url
            return response
        return HttpResponseRedirect(redirect_url)
