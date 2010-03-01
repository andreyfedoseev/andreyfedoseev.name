from django_assets import Bundle

from django.conf import settings
import os.path
from django_assets.registry import register

PREFIX = os.path.join(getattr(settings, "STATIC_DIRNAME", "static"), "blueprint")


blueprint = Bundle(
    os.path.join(PREFIX, 'reset.css'),
    os.path.join(PREFIX, 'typography.css'),
    os.path.join(PREFIX, 'grid.css'),
    os.path.join(PREFIX, 'forms.css'),
    output="gen/blueprint.css"
)

blueprint_print_css = Bundle(
    os.path.join(PREFIX, 'print.css'),
    filters="cssrewrite,cssutils",
    output="gen/blueprint-print.css",
)

blueprint_ie_css = Bundle(
    os.path.join(PREFIX, 'ie.css'),
    output="gen/blueprint-ie.css",
)

register("blueprint", blueprint)