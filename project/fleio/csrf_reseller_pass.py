from django.conf import settings
from django.http.request import split_domain_port
from django.utils.deprecation import MiddlewareMixin


class CsrfMid(MiddlewareMixin):
    def process_request(self, request):
        dom, port = split_domain_port(request.get_host())
        matching_domains = [domain for domain in settings.RESELLER_DOMAINS if dom.endswith(domain)]
        if len(matching_domains) > 0:
            settings.CSRF_COOKIE_DOMAIN = settings.RESELLER_DOMAINS[matching_domains[0]]['cookie_domain']
            settings.CSRF_COOKIE_NAME = 'csrftoken'
        else:
            settings.CSRF_COOKIE_DOMAIN = None
            settings.CSRF_COOKIE_NAME = 'csrftoken'

    def process_response(self, request, response):
        dom, port = split_domain_port(request.get_host())
        matching_domains = [domain for domain in settings.RESELLER_DOMAINS if dom.endswith(domain)]
        if len(matching_domains) > 0:
            settings.CSRF_COOKIE_DOMAIN = settings.RESELLER_DOMAINS[matching_domains[0]]['cookie_domain']
            settings.CSRF_COOKIE_NAME = 'csrftoken'
        else:
            settings.CSRF_COOKIE_DOMAIN = None
            settings.CSRF_COOKIE_NAME = 'csrftoken'
        return response
