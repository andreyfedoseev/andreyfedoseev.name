from django_assets.bundle import Bundle
from blueprint.assets import blueprint
from django_assets.registry import register


error_css = Bundle(
    blueprint,
    'styles/error.css',
    filters="cssrewrite,cssutils",
    output="gen/error.css",
)

register("error_css", error_css)
