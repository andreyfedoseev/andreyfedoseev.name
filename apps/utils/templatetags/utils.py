from django.template import Library


register = Library()


@register.inclusion_tag("utils/include/localized-flatblock.html", takes_context=True)
def localized_flatblock(context, name):
    request = context["request"]
    name = "%s-%s" % (name, request.LANGUAGE_CODE)
    return dict(name=name)


