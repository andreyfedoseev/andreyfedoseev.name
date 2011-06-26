from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils import translation


class LocaleMiddleware(object):

    def __init__(self):
        self.languages = [l[0] for l in settings.LANGUAGES]
        self.default_language = settings.LANGUAGE_CODE

    def get_language(self, request):
        parts = request.path.split("/")
        if parts[1] in self.languages:
            language = parts[1]
        else:
            language = self.default_language
        return language

    def process_request(self, request):
        language = self.get_language(request)
        request.LANGUAGE_CODE = language
        translation.activate(language)
        if language != self.default_language:
            request.urlconf = "%s_%s" % (settings.ROOT_URLCONF, language)
        return None

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = self.get_language(request)
        translation.deactivate()
        return response


