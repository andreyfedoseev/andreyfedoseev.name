from pelican import signals
import gettext
import os


DOMAIN = "messages"


def init_template_translations(generator):
    lang = generator.settings["DEFAULT_LANG"]
    if lang == "en":
        translations = gettext.NullTranslations()
    else:
        translations = gettext.translation(DOMAIN, os.path.join(generator.theme, "translations"), [lang])
    generator.env.install_gettext_translations(translations)


def register():
    signals.generator_init.connect(init_template_translations)
