from blueprint.assets import blueprint, blueprint_print_css, blueprint_ie_css
from django.conf import settings
from django_assets import Bundle, register
from jquery.assets import jquery, jquery_cookie, jquery_url, jquery_ajaxupload, \
    jquery_ui_css, jquery_ui, jquery_markitup_html_css, jquery_markitup_html, \
    jquery_template, jquery_inline_label, jquery_scroll_to, jquery_ui_core, \
    jquery_ui_highlight, jquery_markitup_core, jquery_markitup_markdown, \
    jquery_markitup_markdown_css, jquery_markitup_core_css, jquery_tooltip, \
    jquery_tooltip_css, jquery_history
import os.path



PREFIX = os.path.join(getattr(settings, "STATIC_DIRNAME", "static"), "blog")

blog_frontend_css = Bundle(
    blueprint,
    jquery_markitup_core_css,
    jquery_markitup_markdown_css,
    jquery_tooltip_css,
    os.path.join(PREFIX, 'styles/base.css'),
    os.path.join(PREFIX, 'styles/style.css'),
    os.path.join(PREFIX, 'styles/highlight.css'),
    filters="cssrewrite,cssutils",
    output="gen/frontend.css",
)

blog_frontend_js = Bundle(
    jquery,
    jquery_cookie,
    jquery_url,
    jquery_history,
    jquery_scroll_to,
    jquery_ui_core,
    jquery_ui_highlight,
    jquery_markitup_core,
    jquery_markitup_markdown,
    jquery_tooltip,
    os.path.join(PREFIX, "javascripts/grid.js"),
    os.path.join(PREFIX, "javascripts/comments.js"),
    output="gen/blog-frontend.js",
    filters="jsmin",      
)

blog_admin_css = Bundle(
    blueprint,
    jquery_ui_css,
    jquery_markitup_html_css,
    os.path.join(PREFIX, 'styles/base.css'),
    os.path.join(PREFIX, 'styles/admin-style.css'),
    filters="cssrewrite,cssutils",
    output="gen/admin.css",
)

blog_admin_js = Bundle(
    jquery,
    jquery_template,
    jquery_ui,
    jquery_markitup_html,
    jquery_ajaxupload,
    jquery_inline_label,
    os.path.join(PREFIX, "javascripts/imageswidget.js"),
    output="gen/admin.js",
    filters="jsmin",      
)

register("blog_frontend_css", blog_frontend_css)
register("blog_frontend_js", blog_frontend_js)
register("blog_admin_css", blog_admin_css)
register("blog_admin_js", blog_admin_js)
register("blog_print_css", blueprint_print_css)
register("blog_ie_css", blueprint_ie_css)

