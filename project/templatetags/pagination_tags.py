from django import template

register = template.Library()

@register.inclusion_tag('components/pagination.html')
def render_pagination(page_obj, page_param='page'):
    return {
        'page_obj': page_obj,
        'page_param': page_param,
    }
