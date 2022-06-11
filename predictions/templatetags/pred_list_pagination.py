from atexit import register
from django import template # type: ignore

register = template.Library()


@register.simple_tag
def filtered_page_url(page_num, querystring=None):
    url = f'?page={page_num}'

    if querystring:
        filters = querystring.split('&')
        filters = [q for q in filters if q.split('=')[0] != 'page']
        qs = '&'.join(filters)
        url += f'&{qs}'

    return url