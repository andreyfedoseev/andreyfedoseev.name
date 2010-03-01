from django_assets import Bundle
from django.conf import settings
import os.path

PREFIX = os.path.join(getattr(settings, "STATIC_DIRNAME", "static"), "jquery")


jquery = Bundle(
    os.path.join(PREFIX, 'jquery-1.4.js'),
    os.path.join(PREFIX, 'jquery.json-2.2.js'),
    os.path.join(PREFIX, 'jquery.delay.js'),
    os.path.join(PREFIX, 'jquery.bgiframe.js'),
    os.path.join(PREFIX, 'jquery.delegate.js'),
    os.path.join(PREFIX, 'jquery.dimensions.js'),
    output="gen/jquery.js"
)

jquery_ui_core = Bundle(
    os.path.join(PREFIX, 'jquery-ui/ui/ui.core.js'),
    os.path.join(PREFIX, 'jquery-ui/ui/effects.core.js'),
    output="gen/jquery-ui.core.js"                
)

jquery_ui_css_core = Bundle(
    os.path.join(PREFIX, 'jquery-ui/themes/base/ui.core.css'),
    os.path.join(PREFIX, 'jquery-ui/themes/base/ui.theme.css'),
    output="gen/jquery-ui.core.css",
    filters="cssrewrite,cssutils"
)

jquery_ui = Bundle(
    jquery_ui_core,                   
    os.path.join(PREFIX, 'jquery-ui/ui/ui.datepicker.js'),
    os.path.join(PREFIX, 'jquery-ui/ui/ui.dialog.js'),
    output="gen/jquery-ui.js"                
)


jquery_ui_css = Bundle(
    jquery_ui_css_core,
    os.path.join(PREFIX, 'jquery-ui/themes/base/ui.datepicker.css'),
    os.path.join(PREFIX, 'jquery-ui/themes/base/ui.dialog.css'),
    output="gen/jquery-ui.css",
    filters="cssrewrite,cssutils"
)

jquery_ui_modal = Bundle(
    os.path.join(PREFIX, 'jquery-ui/ui/ui.droppable.js'),
    output="gen/jquery-ui.dnd.js"                
)

jquery_ui_dnd = Bundle(
    os.path.join(PREFIX, 'jquery-ui/ui/ui.draggable.js'),
    os.path.join(PREFIX, 'jquery-ui/ui/ui.droppable.js'),
    output="gen/jquery-ui.dnd.js"                
)

jquery_ui_highlight = Bundle(
    os.path.join(PREFIX, 'jquery-ui/ui/effects.highlight.js'),
    output="gen/jquery-ui.highlight.js"                
)

jquery_form = Bundle(
    os.path.join(PREFIX, 'jquery.form.js'),
    output="gen/jquery.form.js"                
)

jquery_ajaxupload = Bundle(
    os.path.join(PREFIX, 'ajaxupload.js'),
    output="gen/jquery.ajaxupload.js"                
)

jquery_template = Bundle(
    os.path.join(PREFIX, 'jquery.template.js'),
    output="gen/jquery.template.js"                
)

jquery_cookie = Bundle(
    os.path.join(PREFIX, 'jquery.cookie.js'),
    output="gen/jquery.cookie.js"                
)

jquery_url = Bundle(
    os.path.join(PREFIX, 'jquery.url.js'),
    output="gen/jquery.url.js"                
)

jquery_markitup_core = Bundle(
    os.path.join(PREFIX, 'markitup/jquery.markitup.js'),
    output="gen/jquery.markitup.js"                
)

jquery_markitup_core_css = Bundle(
    os.path.join(PREFIX, 'markitup/skins/simple/style.css'),
    output="gen/jquery.markitup.css",                
    filters="cssrewrite,cssutils"
)

jquery_markitup_default = Bundle(
    jquery_markitup_core,
    os.path.join(PREFIX, 'markitup/sets/default/set.js'),                                    
    output="gen/jquery.markitup-default.js",                
)

jquery_markitup_default_css = Bundle(
    jquery_markitup_core_css,
    os.path.join(PREFIX, 'markitup/sets/default/style.css'),                                    
    output="gen/jquery.markitup-default.css",                
)

jquery_markitup_html = Bundle(
    jquery_markitup_core,
    os.path.join(PREFIX, 'markitup/sets/html/set.js'),                                    
    output="gen/jquery.markitup-html.js",                
)

jquery_markitup_html_css = Bundle(
    jquery_markitup_core_css,
    os.path.join(PREFIX, 'markitup/sets/html/style.css'),                                    
    output="gen/jquery.markitup-html.css",                
)

jquery_markitup_markdown = Bundle(
    jquery_markitup_core,
    os.path.join(PREFIX, 'markitup/sets/markdown/set.js'),                                    
    output="gen/jquery.markitup-markdown.js",                
)

jquery_markitup_markdown_css = Bundle(
    jquery_markitup_core_css,
    os.path.join(PREFIX, 'markitup/sets/markdown/style.css'),                                    
    output="gen/jquery.markitup-markdown.css",                
)

jquery_inline_label = Bundle(
    os.path.join(PREFIX, 'jquery.inline_label.js'),                                    
    output="gen/jquery.inline_label.js",                
)

jquery_scroll_to = Bundle(
    os.path.join(PREFIX, 'jquery.scrollTo.js'),                                    
    output="gen/jquery.scrollTo.js",                
)

jquery_tooltip = Bundle(
    os.path.join(PREFIX, 'jquery-tooltip/jquery.tooltip.js'),                                    
    output="gen/jquery.tooltip.js",                
)

jquery_tooltip_css = Bundle(
    os.path.join(PREFIX, 'jquery-tooltip/jquery.tooltip.css'),                                    
    output="gen/jquery.tooltip.css",                
)
