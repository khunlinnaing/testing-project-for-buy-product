from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_name_in(context, *names):
    try:
        current = context['request'].resolver_match.url_name
        return current in names
    except (AttributeError, KeyError):
        return False
