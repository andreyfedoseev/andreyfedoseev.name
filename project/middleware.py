from django.conf import settings
from django.middleware.locale import LocaleMiddleware as BaseLocaleMiddleware


class LocaleMiddleware(BaseLocaleMiddleware):

    def __init__(self):
        self.languages = [l[0] for l in settings.LANGUAGES]
        self.default_language = settings.LANGUAGE_CODE

    def process_request(self, request):
        parts = request.path.split("/")
        if parts[1] in self.languages:
            language = parts[1]
        else:
            language = self.default_language

        request.LANGUAGE_CODE = language
        if language != self.default_language:
            request.urlconf = "project.urls_%s" % language

        return None



